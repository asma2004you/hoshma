# -*- coding: utf-8 -*-
"""
عامل واکنشی ساده براي مسئله کليد نور در محيط 2*2
هدف عامل: خاموش کردن همه خانه‌هاي روشن

ساختار الگوریتم:
    اکشن = f(ادراک لحظه‌ای)   # بدون حافظه و بدون مدل محیط

قواعد شرط–اکشن (با اولویت از بالا به پایین):
    IF خانه فعلی روشن است            -> TOGGLE
    ELSE IF خانه‌ای روشن دیگر هست    -> حرکت به سمت نزدیک‌ترین خانه روشن
    ELSE                             -> NOOP (پایان)
"""

from __future__ import annotations

import random
from typing import List, Tuple

Pos = Tuple[int, int]
Grid = List[List[bool]]

ACTIONS = ("TOGGLE", "UP", "DOWN", "LEFT", "RIGHT", "NOOP")
MOVES = {"UP": (-1, 0), "DOWN": (1, 0), "LEFT": (0, -1), "RIGHT": (0, 1)}


# ----------------------------------------------------------------------------
# محيط: شبکه 2*2 که هر خانه يک کليد نور دارد
# ----------------------------------------------------------------------------
class LightSwitchEnv:
    def __init__(self, lights: Grid | None = None, start: Pos = (0, 0)) -> None:
        self.n = 2
        base = lights if lights is not None else [[True, True], [True, False]]
        self.lights: Grid = [row[:] for row in base]
        self.pos: Pos = start
        self.steps = 0
        self.done = False

    def perceive(self) -> dict:
        """ادراک کامل: وضعیت همه چراغ‌ها + موقعیت خود عامل."""
        return {"lights": [row[:] for row in self.lights], "pos": self.pos}

    def step(self, action: str):
        """اعمال اکشن عامل، سپس بازگشت ادراک جدید و نشان پایان."""
        if action not in ACTIONS:
            raise ValueError(f"اکشن نامعتبر: {action}")

        r, c = self.pos
        if action == "TOGGLE":
            self.lights[r][c] = not self.lights[r][c]
        elif action in MOVES:
            dr, dc = MOVES[action]
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.n and 0 <= nc < self.n:
                self.pos = (nr, nc)
            # خارج از شبکه -> برخورد (bump): در جا می‌ماند
        # NOOP: کاری انجام نمی‌شود

        self.steps += 1
        if not any(any(row) for row in self.lights):  # همه خاموش؟
            self.done = True
        return self.perceive(), self.done

    def render(self) -> str:
        lines = []
        for r in range(self.n):
            row = []
            for c in range(self.n):
                cell = "O" if self.lights[r][c] else "."  # O=روشن, .=خاموش
                row.append(f"[{cell}]" if (r, c) == self.pos else f" {cell} ")
            lines.append(" ".join(row))
        return "\n".join(lines)


# ----------------------------------------------------------------------------
# عامل واکنشی ساده: تابع خالص ادراک -> اکشن (بدون هیچ حافظه‌ای)
# ----------------------------------------------------------------------------
class SimpleReactiveAgent:
    def decide(self, percept: dict) -> str:
        r, c = percept["pos"]
        lights = percept["lights"]

        # قاعده ۱: خانه فعلی روشن است -> خاموشش کن
        if lights[r][c]:
            return "TOGGLE"

        # قاعده ۲: هنوز خانه روشن دیگری هست -> برو سمت نزدیک‌ترین آن
        lit = [(rr, cc) for rr in range(2) for cc in range(2) if lights[rr][cc]]
        if lit:
            tr, tc = min(lit, key=lambda p: (abs(p[0] - r) + abs(p[1] - c), p))
            if tr != r:
                return "UP" if tr < r else "DOWN"
            return "LEFT" if tc < c else "RIGHT"

        # قاعده ۳: همه خاموش‌اند -> توقف
        return "NOOP"


# ----------------------------------------------------------------------------
# حلقه اجرا: ادراک -> تصمیم -> اکشن -> تغییر محیط -> ...
# ----------------------------------------------------------------------------
def run(env: LightSwitchEnv, agent: SimpleReactiveAgent, verbose: bool = True) -> int:
    if verbose:
        print("وضعیت اولیه:")
        print(env.render())
        print("-" * 30)

    while not env.done:
        percept = env.perceive()
        action = agent.decide(percept)
        if verbose:
            print(f"قدم {env.steps + 1}: ادراک pos={percept['pos']} "
                  f"lights={percept['lights']}  ->  اکشن: {action}")
        if action == "NOOP" and not env.done:
            raise RuntimeError("عامل تسلیم شد ولی هنوز چراغ روشن هست!")
        env.step(action)
        if verbose:
            print(env.render())
            print("-" * 30)

    if verbose:
        print(f"پایان در {env.steps} قدم: همه خانه‌ها خاموش شدند ✔")
    return env.steps


def main() -> None:
    print("=" * 40)
    print("اجراي نمونه اوليه")
    print("=" * 40)
    env = LightSwitchEnv(lights=[[True, True], [True, True]], start=(0, 0))
    run(env, SimpleReactiveAgent(), verbose=True)

    print()
    print("=" * 40)
    print("آزمون 100 محيط تصادفي")
    print("=" * 40)
    random.seed(42)
    worst = 0
    for i in range(100):
        lights = [[random.random() < 0.5 for _ in range(2)] for _ in range(2)]
        start = (random.randrange(2), random.randrange(2))
        e = LightSwitchEnv(lights=lights, start=start)
        if not any(any(row) for row in lights):  # حالت از پیش خاموش
            continue
        steps = run(e, SimpleReactiveAgent(), verbose=False)
        assert not any(any(row) for row in e.lights), "خطا: چراغی روشن ماند!"
        worst = max(worst, steps)
    print("همه 100 آزمون موفق بودند. بیشترین تعداد قدم:", worst)


if __name__ == "__main__":
    main()
