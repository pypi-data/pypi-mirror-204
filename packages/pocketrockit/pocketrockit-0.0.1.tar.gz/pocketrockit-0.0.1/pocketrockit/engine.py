#!/usr/bin/env python3

"""Demonstrates the midi music player

https://newt.phys.unsw.edu.au/jw/notes.html

"""

import asyncio
import concurrent
import logging
import threading
from asyncio import sleep
from collections.abc import Iterable
from contextlib import ExitStack, contextmanager, suppress
from importlib.util import module_from_spec, spec_from_file_location
from itertools import count
from pathlib import Path

import fluidsynth
import pygame.midi
from asyncinotify import Inotify, Mask


@contextmanager
def mididevice_pygame():
    """
    fluidsynth -vv -a pipewire -z 256 -g 2 FluidR3_GM.sf2
    """
    try:
        pygame.midi.init()
        for i in range(pygame.midi.get_count()):
            print(pygame.midi.get_device_info(i))
        player = pygame.midi.Output(2)
        player.set_instrument(0)
        yield player
    finally:
        del player
        pygame.midi.quit()


@contextmanager
def mididevice_fluidsynth():
    """
    Todo: make behave like subprocess
    """
    try:
        midi_out = fluidsynth.Synth(gain=2.0, samplerate=44100.0)
        midi_out.setting("audio.period-size", 256)
        midi_out.start(driver="pulseaudio")
        midi_out.program_select(0, midi_out.sfload("FluidR3_GM.sf2"), 0, 0)
        midi_out.program_select(1, midi_out.sfload("JV_1080_Drums.sf2"), 128, 0)
        yield midi_out
    finally:
        midi_out.delete()


def pygame_thread_fn(loop, event_queue, terminator):
    """Pygame thread"""
    try:
        logger().debug(">> pygame_thread_fn")
        pygame.init()
        pygame.display.set_caption("pygame+asyncio")
        screen = pygame.display.set_mode((512, 512))

        while not terminator.is_set():
            event = pygame.event.wait()
            asyncio.run_coroutine_threadsafe(event_queue.put(event), loop=loop)

        logger().debug("pygame_thread_fn: got termination signal")

    except Exception as exc:
        logger().error("Unhandled exception in pygame thread: %s", exc)
        raise

    finally:
        logger().debug("pygame.quit()")
        pygame.quit()

        logger().debug("<< pygame_thread_fn")


def choose(choices: Iterable[str], *wishlist: str) -> str:
    for wish in wishlist:
        with suppress(StopIteration):
            return next(name for name in choices if wish in name)
    raise KeyError(f"{wishlist}")


def read_midi(loop, event_queue, terminator):
    logger().debug(">> read_midi")

    try:
        available_input_ports = set(mido.get_input_names())
        logger().info("Available MIDI input ports: \n%s", "  \n".join(available_input_ports))

        chosen_input = choose(
            available_input_ports, "OP-1", "Sylphyo", "USB MIDI Interface", "Midi Through"
        )
        logger().info("Chosen: %r", chosen_input)

        with mido.open_input(chosen_input) as inport:
            while not terminator.is_set():
                if (event := inport.receive()).type == "clock":
                    continue
                asyncio.run_coroutine_threadsafe(event_queue.put(event), loop=loop)
            logger().debug("read_midi: got termination signal")

    except Exception as exc:
        logger().error("Unhandled exception in read_midi thread: %s", exc)

    logger().debug("<< read_midi")


async def handle_events(event_queue, task, terminator):
    logger().debug(">> handle_events")
    try:
        while not terminator.is_set():
            try:
                event = await event_queue.get()
                if event.type in {pygame.WINDOWCLOSE, pygame.QUIT}:
                    logger().debug("quit/windowclose")
                    terminate(terminator)
                #        elif event.type == pygame.KEYDOWN:
                #            if event.key == pygame.K_SPACE:
                #                if ball.speed == [0, 0]:
                #                    ball.speed = [2, 2]
                #                else:
                #                    ball.speed = [0, 0]
                elif event.type == pygame.MOUSEMOTION:
                    pass
                elif event.type == pygame.TEXTINPUT:
                    pass
                elif event.type == pygame.KEYDOWN:
                    pass
                elif event.type == pygame.KEYUP:
                    pass
                elif event.type == "note_on":
                    print("NOTEON", event)
                elif event.type == "note_off":
                    print("NOTEOFF", event)
                else:
                    logger().debug("event %s", event)
            except Exception as exc:
                print(exc)
        logger().debug("handle_events: got termination signal")

    finally:
        # Close the connection to the output device and quit the MIDI system
        # midi_out.delete()

        asyncio.get_event_loop().stop()
        logger().debug("<< handle_events")


def terminate(terminator):
    terminator.set()
    pygame.event.post(pygame.event.Event(pygame.MOUSEMOTION))


def logger():
    return logging.getLogger("silmaril")


def setup_logging():
    def thread_id_filter(record):
        """Inject thread_id to log records"""
        record.thread_id = threading.get_native_id()
        return record

    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter("%(asctime)s | %(levelname)s | %(thread_id)s | %(message)s")
    )
    handler.addFilter(thread_id_filter)
    logger().addHandler(handler)
    logger().setLevel("DEBUG")


def load_module(filepath: str | Path):
    print(r"load module '{Path(filepath).stem}'")
    spec = spec_from_file_location(Path(filepath).stem, filepath)
    module = module_from_spec(spec)
    # here the actual track definition takes place
    spec.loader.exec_module(module)
    return module


async def tick(singleton):
    with mididevice_fluidsynth() as midi_out:
        # wait for players to emerge (otherwise `tick` won't start at 0)
        while True:
            if singleton.players:
                break
            print("no players yet..")
            await sleep(1)
            continue

        for tick in count():
            singleton.tick = tick

            notes = []
            if tick % 1 == 0:
                print(f"== {tick // 16} {tick // 4} {tick % 4} {tick} ==")

            for name, stream in singleton.players:
                try:
                    source_loop, source_tick, origin, commands = next(stream)
                    print(f"{name}: {source_loop}:{source_tick}:{origin} => {commands}")
                    if commands:
                        notes.extend(commands)
                except StopIteration:
                    pass
                except Exception as exc:
                    print(f"exception in play: {exc}")
                    print("--")

            for note in notes:
                midi_out.noteon(*note)

            # make me absolute please
            await sleep(0.2)


async def watch_changes(filepath):
    load_module(filepath)
    with Inotify() as inotify:
        inotify.add_watch(
            Path(filepath).parent,
            Mask.CLOSE_WRITE,
        )
        async for event in inotify:
            print(event.path, event.mask)
            try:
                load_module(event.path)
            except Exception as exc:
                print("caught {exc}")


def run(singleton):
    setup_logging()
    logger().info("Hello from main thread")
    event_queue = asyncio.Queue()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    terminator = threading.Event()

    with ExitStack() as context:
        # context.enter_context(setup_midi(event_queue))
        pool = context.enter_context(concurrent.futures.ThreadPoolExecutor())

        midi_reader = loop.run_in_executor(pool, read_midi, loop, event_queue, terminator)
        pygame_task = (
            None  # loop.run_in_executor(pool, pygame_thread_fn, loop, event_queue, terminator)
        )
        event_task = asyncio.ensure_future(handle_events(event_queue, pygame_task, terminator))
        asyncio.ensure_future(tick(singleton))
        asyncio.ensure_future(watch_changes(singleton.file_to_track))

        try:
            loop.run_forever()
        except KeyboardInterrupt:
            logger().debug("KeyboardInterrput in main()")
            terminate(terminator)

        finally:
            logger().debug("finally - loop.run_forever()")
