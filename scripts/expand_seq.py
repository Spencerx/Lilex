#!/usr/bin/env python3
"""Expand sequential glyphs"""

from argparse import ArgumentParser
from pathlib import Path

from glyphsLib import GSFont, GSNode, GSPath

ENDINGS = (610, -610, -10)


def main() -> None:
    parser = ArgumentParser(description="Expand sequential glyphs in a .glyphs file")
    parser.add_argument("path", type=Path, help="Path to the .glyphs file")
    parser.add_argument(
        "--size",
        "-s",
        type=float,
        help="Value to expand by",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        help="Path to the output .glyphs file",
    )
    args = parser.parse_args()

    font = GSFont(args.path)
    for glyph in font.glyphs:
        is_modified = False
        if glyph.name.endswith(".seq"):
            for layer in glyph.layers:
                for shape in layer.shapes:
                    if not isinstance(shape, GSPath):
                        continue
                    if not is_modified:
                        print(f"Expanding {glyph.name}")
                        is_modified = True
                    for node in shape.nodes:
                        node: GSNode = node
                        x = node.position.x
                        if x in ENDINGS:
                            if x > 0:
                                node.position.x += args.size
                            else:
                                node.position.x -= args.size

    if args.output:
        font.save(args.output)


if __name__ == "__main__":
    main()
