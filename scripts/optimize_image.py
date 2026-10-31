#!/usr/bin/env python3
"""
이미지 최적화 자동화 스크립트 (Image Optimization Tool)
- 고해상도 마스터 이미지를 웹 화면 표시 크기 및 고해상도(Retina 2x~3x)에 맞게 리사이징
- 차세대 웹 포맷인 WebP 변환 및 최적화된 PNG 파일 동시 생성
- 목표: 초기 로딩 시간 단축, Core Web Vitals (LCP) 개선, 대역폭 절약
"""

import os
import sys
import argparse
from PIL import Image

def optimize_image(input_path, output_dir=None, max_size=256, quality=92, keep_png=True):
    if not os.path.isfile(input_path):
        print(f"[Error] 파일이 존재하지 않습니다: {input_path}")
        return False

    orig_size = os.path.getsize(input_path)
    base_name = os.path.splitext(os.path.basename(input_path))[0]
    
    if output_dir is None:
        output_dir = os.path.dirname(input_path)
    os.makedirs(output_dir, exist_ok=True)

    with Image.open(input_path) as img:
        w, h = img.size
        print(f"\n[입력 파일] {input_path}")
        print(f"  - 원본 규격: {w}x{h} px")
        print(f"  - 원본 용량: {orig_size:,} bytes ({orig_size / 1024:.1f} KB)")

        # 비율 유지 리사이즈 계산
        if max(w, h) > max_size:
            ratio = max_size / max(w, h)
            new_w = max(1, int(w * ratio))
            new_h = max(1, int(h * ratio))
            resized = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
            print(f"  - 리사이즈: {new_w}x{new_h} px (최대 상한 {max_size}px 적용)")
        else:
            resized = img
            new_w, new_h = w, h
            print(f"  - 크기 유지: {w}x{h} px (이미 상한 이하)")

        # 1. WebP 저장
        webp_path = os.path.join(output_dir, f"{base_name}.webp")
        # RGBA 유지 또는 투명도 없는 경우 RGB
        if resized.mode in ("RGBA", "LA") or (resized.mode == "P" and "transparency" in resized.info):
            save_img = resized
        else:
            save_img = resized.convert("RGB")

        save_img.save(webp_path, "WEBP", quality=quality, method=6)
        webp_size = os.path.getsize(webp_path)
        reduction = (1 - webp_size / orig_size) * 100
        print(f"  - [WebP 생성] {webp_path}")
        print(f"    용량: {webp_size:,} bytes ({webp_size / 1024:.1f} KB) | 감축률: {reduction:.1f}%")

        # 2. PNG 최적화 저장 (옵션)
        if keep_png:
            png_path = os.path.join(output_dir, f"{base_name}.png")
            save_img.save(png_path, "PNG", optimize=True)
            png_size = os.path.getsize(png_path)
            png_reduction = (1 - png_size / orig_size) * 100
            print(f"  - [PNG 최적화] {png_path}")
            print(f"    용량: {png_size:,} bytes ({png_size / 1024:.1f} KB) | 감축률: {png_reduction:.1f}%")

    return True

def main():
    parser = argparse.ArgumentParser(description="웹 성능 최적화용 이미지 자동 리사이즈 및 WebP 변환기")
    parser.add_argument("input", help="최적화할 원본 이미지 경로")
    parser.add_argument("-o", "--output", default=None, help="출력 디렉토리 (기본값: 원본 경로 디렉토리)")
    parser.add_argument("-s", "--max-size", type=int, default=256, help="최대 너비/높이 픽셀 (기본: 256)")
    parser.add_argument("-q", "--quality", type=int, default=92, help="WebP 압축 품질 (1-100, 기본: 92)")
    parser.add_argument("--no-png", action="store_true", help="PNG 대체 파일 생성 안함")

    args = parser.parse_args()
    optimize_image(args.input, args.output, args.max_size, args.quality, not args.no_png)

if __name__ == "__main__":
    main()
