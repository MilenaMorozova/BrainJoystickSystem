from unittest.mock import MagicMock

from helpers.timer import Timer


def test_signals_emitting(qtbot):
    on_tick_handler = MagicMock()
    timer = Timer(1.05)
    timer.on_tick.connect(on_tick_handler)

    with qtbot.waitSignal(timer.on_end, timeout=2000):
        timer.start()

    assert on_tick_handler.call_count == 10   # (1 * 1000 / Timer.TICK_TIME)
