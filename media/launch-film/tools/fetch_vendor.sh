#!/bin/bash
# Fetch the film's JavaScript library and fonts at the versions it was built with, and check each file
# against the copy that rendered the film (SHA-256). Run from media/launch-film/.
set -euo pipefail
cd "$(dirname "$0")/.."

fetch() {  # url  destination  sha256
  mkdir -p "$(dirname "$2")"
  curl -fsSL "$1" -o "$2.tmp"
  got=$(shasum -a 256 "$2.tmp" | cut -d' ' -f1)
  if [ "$got" != "$3" ]; then
    rm -f "$2.tmp"
    echo "checksum mismatch for $1" >&2
    exit 1
  fi
  mv "$2.tmp" "$2"
  echo "ok  $2"
}

GSAP=https://cdn.jsdelivr.net/npm/gsap@3.14.2
INTER=https://cdn.jsdelivr.net/gh/rsms/inter@v4.1

fetch "$GSAP/dist/gsap.min.js" assets/vendor/gsap.min.js \
  c174bfce53a729418d57a8ad8625e7247c793a22fef8e2851e3cfa3de9cd8280
fetch "$INTER/docs/font-files/Inter-Regular.woff2" assets/fonts/Inter-Regular.woff2 \
  e06f6b1bc553aaea4e4668023ed0ab0a147129c3107f511bc7d03d361b0ae085
fetch "$INTER/docs/font-files/Inter-Medium.woff2" assets/fonts/Inter-Medium.woff2 \
  0ff3e94614e1493eb556314fd247ae6c4a85a7783b4cc86be539940cf83f2a48
fetch "$INTER/docs/font-files/Inter-SemiBold.woff2" assets/fonts/Inter-SemiBold.woff2 \
  5cb7103e4e605989afebc03d989c79201e54b21b5183db33981f70db9178a301
fetch "$INTER/docs/font-files/InterDisplay-SemiBold.woff2" assets/fonts/InterDisplay-SemiBold.woff2 \
  d9f63a82b826fb0117c92715c3a52a2d2247bc321bc39341420bf52d91e8277a
fetch "$INTER/LICENSE.txt" assets/fonts/OFL-Inter.txt \
  262481e844521b326f5ecd053e59b98c8b2da78c8ee1bdbb6e8174305e54935a
