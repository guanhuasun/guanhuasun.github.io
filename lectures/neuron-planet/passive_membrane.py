"""Lecture 1: passive membrane simulation with no third-party dependencies.

Run: python passive_membrane.py
Check the implementation: python passive_membrane.py --self-test

Units throughout: ms, mV, nA, nF, microSiemens.
This is a single-compartment, constant-conductance model, with no spike rule.
"""
import argparse
import csv
import math
from pathlib import Path


def applied_current(t, amplitude=0.10, on=10.0, off=60.0):
    """Inward-positive rectangular injected current, in nA."""
    return amplitude if on - 1e-9 <= t < off - 1e-9 else 0.0


def exact_voltage(t, C=0.10, g=0.010, E=-65.0,
                  amplitude=0.10, on=10.0, off=60.0):
    """Analytic solution, starting at E, including pulse switch-off."""
    tau = C / g
    if t <= on:
        return E
    if t <= off:
        return E + amplitude / g * (1 - math.exp(-(t - on) / tau))
    at_off = E + amplitude / g * (1 - math.exp(-(off - on) / tau))
    return E + (at_off - E) * math.exp(-(t - off) / tau)


def simulate(C=0.10, g=0.010, E=-65.0, amplitude=0.10,
             on=10.0, off=60.0, dt=0.10, duration=100.0):
    """Forward Euler. The old voltage and current determine each update."""
    if not all(math.isfinite(x) for x in (C, g, E, amplitude, on, off, dt, duration)):
        raise ValueError("All parameters must be finite.")
    if min(C, g, dt, duration) <= 0:
        raise ValueError("C, g, dt, and duration must be positive.")
    if not 0 <= on < off <= duration:
        raise ValueError("Require 0 <= pulse onset < pulse offset <= duration.")
    if duration / dt > 100_000:
        raise ValueError("Too many steps for this teaching example.")
    voltage = E
    rows = []
    count = math.ceil(duration / dt)
    for k in range(count + 1):
        t = min(k * dt, duration)
        current = applied_current(t, amplitude, on, off)
        leak = g * (voltage - E)  # outward-positive leak current
        exact = exact_voltage(t, C, g, E, amplitude, on, off)
        rows.append((t, current, voltage, exact, leak))
        if k < count:
            step = min(dt, duration - t)
            voltage += step * (current - leak) / C
    return rows


def write_svg(rows, destination):
    """Write an offline, labeled vector plot directly from numerical samples."""
    width, height, left, right = 960, 620, 105, 910
    duration = rows[-1][0]
    lo = min(-67.0, min(row[2] for row in rows) - 2)
    hi = max(-53.0, max(row[2] for row in rows) + 2)
    low_i, high_i = min(0.0, min(r[1] for r in rows)), max(0.05, max(r[1] for r in rows))
    x = lambda t: left + (right - left) * t / duration
    y = lambda v: 540 - (v - lo) / (hi - lo) * 290
    yi = lambda i: 185 - (i - low_i) / (high_i - low_i) * 100
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
             '<title>Passive membrane: Euler simulation and analytical reference</title>',
             '<rect width="100%" height="100%" fill="#f6f5f0"/>',
             '<g font-family="Arial,sans-serif" font-size="18" fill="#202523">',
             '<text x="105" y="38" font-size="25">Passive membrane · illustrative model simulation</text>']
    for top, bottom in ((75, 195), (250, 540)):
        parts.append(f'<path d="M{left} {top} V{bottom} H{right}" fill="none" stroke="#626c68"/>')
    for k in range(6):
        t = k * duration / 5
        parts.append(f'<text x="{x(t)}" y="570" text-anchor="middle">{t:g}</text>')
    for k in range(4):
        v = lo + (hi - lo) * k / 3
        parts.append(f'<text x="90" y="{y(v)+6}" text-anchor="end">{v:.1f}</text>')
    for val in sorted(set((low_i, high_i, 0.0))):
        parts.append(f'<text x="90" y="{yi(val)+6}" text-anchor="end">{val:g}</text>')
    for column, transform, color, dash in ((1, yi, '#c23b22', ''), (3, y, '#2f6f4e', 'stroke-dasharray="8 6"'), (2, y, '#1e5aa8', '')):
        path = ' '.join(f'{"M" if i == 0 else "L"}{x(r[0]):.2f} {transform(r[column]):.2f}' for i, r in enumerate(rows))
        parts.append(f'<path d="{path}" fill="none" stroke="{color}" stroke-width="2.6" {dash}/>')
    parts.extend(['<text x="18" y="92">I (nA)</text>', '<text x="18" y="270">V (mV)</text>',
                  '<text x="500" y="605" text-anchor="middle">Time (ms)</text>',
                  '<text x="110" y="226" fill="#1e5aa8">Blue: Euler</text>',
                  '<text x="300" y="226" fill="#2f6f4e">Green dashed: exact solution</text>', '</g></svg>'])
    destination.write_text('\n'.join(parts), encoding='utf-8')


def self_test():
    rows = simulate()
    assert len(rows) == 1001 and abs(rows[-1][0] - 100) < 1e-9
    assert all(abs(row[2] + 65) < 1e-9 for row in rows if row[0] <= 10)
    assert abs(rows[101][2] - (-64.9)) < 1e-9
    assert max(abs(r[2] - r[3]) for r in rows) < 0.02
    fine = simulate(dt=0.05)
    assert max(abs(r[2] - r[3]) for r in fine) < max(abs(r[2] - r[3]) for r in rows)
    assert all(abs(r[2] + 65) < 1e-9 for r in simulate(amplitude=0))
    print('Passed: initial state, first Euler step, analytical agreement, convergence, and zero input.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--self-test', action='store_true')
    parser.add_argument('--output-dir', type=Path, default=Path(__file__).resolve().parent / 'demo-output')
    parser.add_argument('--dt', type=float, default=0.1)
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return
    rows = simulate(dt=args.dt)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    with (args.output_dir / 'passive_membrane.csv').open('w', newline='', encoding='utf-8') as stream:
        writer = csv.writer(stream)
        writer.writerow(['time_ms', 'I_app_nA', 'V_euler_mV', 'V_exact_mV', 'I_leak_nA'])
        writer.writerows(rows)
    write_svg(rows, args.output_dir / 'passive_membrane.svg')
    error = max(abs(r[2] - r[3]) for r in rows)
    print(f'Maximum voltage error at sample times: {error:.6f} mV')
    print(f'Wrote CSV and SVG to: {args.output_dir.resolve()}')


if __name__ == '__main__':
    main()
