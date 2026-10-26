#!/usr/bin/env bash
# Read-only project capture. Streams tar -> gzip -> parts; no unsplit archive.
# Usage: bash package-neuron-v16_2.sh [project-directory] [output-parent]
set -Eeuo pipefail
umask 077
export LC_ALL=C

PROJECT="${1:-/home/exnulla/neuron-v16.2}"
OUTPUT_PARENT="${2:-/mnt/c/Users/AdLibitumVita/Downloads}"
PART_BYTES="${NEURON_PART_BYTES:-450000000}"
OUT=""

fail() { printf 'ERROR: %s\n' "$*" >&2; exit 1; }
on_exit() {
    local rc=$?
    if (( rc != 0 )) && [[ -n "$OUT" && -d "$OUT" ]]; then
        printf 'INCOMPLETE: packaging exited with status %s. Do not treat these parts as a finished capture.\n' "$rc" > "$OUT/FAILED.txt" || true
        printf '\nCapture FAILED. Partial output and diagnostics remain in:\n%s\n' "$OUT" >&2
        if [[ -s "$OUT/TAR-LOG.txt" ]]; then tail -n 20 "$OUT/TAR-LOG.txt" >&2 || true; fi
        printf 'Resolve any read errors. If files changed, pause writers/stop Neuron normally and rerun.\n' >&2
    fi
}
trap on_exit EXIT
trap 'exit 130' INT
trap 'exit 143' TERM

(( $# <= 2 )) || fail 'Usage: bash package-neuron-v16_2.sh [project-directory] [output-parent]'
[[ "$PART_BYTES" =~ ^[1-9][0-9]{0,8}$ ]] || fail 'Invalid NEURON_PART_BYTES.'
(( PART_BYTES <= 450000000 )) || fail 'Part sizes must not exceed 450,000,000 bytes.'
for cmd in tar gzip split sha256sum realpath mktemp date du find sort sed stat cat tail df wc; do
    command -v "$cmd" >/dev/null 2>&1 || fail "Required command not found: $cmd"
done
[[ -d "$PROJECT" ]] || fail "Project directory not found: $PROJECT (pass the correct path as the first argument)."
[[ -d "$OUTPUT_PARENT" ]] || fail "Output directory not found: $OUTPUT_PARENT"
PROJECT="$(realpath -e -- "$PROJECT")"
OUTPUT_PARENT="$(realpath -e -- "$OUTPUT_PARENT")"
[[ "$PROJECT" != / ]] || fail 'Refusing to archive the filesystem root.'
case "$OUTPUT_PARENT/" in
    "$PROJECT/"*) fail 'Output must be outside the project, to prevent recursive archive growth.' ;;
esac

OUT="$(mktemp -d -- "$OUTPUT_PARENT/neuron-v16.2-review-$(date -u +%Y%m%dT%H%M%SZ)-XXXXXX")"
SOURCE_PARENT="${PROJECT%/*}"
SOURCE_PARENT="${SOURCE_PARENT:-/}"
SOURCE_NAME="${PROJECT##*/}"
PREFIX='neuron-v16.2.tar.gz.part-'

cat > "$OUT/READ-ME.txt" <<EOF
NEURON V16.2 REVIEW CAPTURE
Started UTC: $(date -u +%FT%TZ)
Source directory: $PROJECT
Part limit: $PART_BYTES bytes (default 450 MB decimal; below 512 MB).

Scope: the entire selected directory, with NO path exclusions. Includes hidden
files, .git, dependencies, logs, old artifacts and local database files.
Symlinks are stored as links, NOT followed. See SYMLINKS.tsv for targets.
External database servers/volumes and other directories are NOT captured.
No services, tests, project code, or database commands are started by this script.
No source files are intentionally written or deleted. No secrets are redacted.

Pause the builders and stop Neuron normally BEFORE capture. Reading a live
project is not an atomic database snapshot. A passed archive check establishes
archive integrity, not application/database consistency.

DIRECTORY-SIZES.txt: allocated directory sizes, two levels deep.
LARGEST-FILES.tsv: 150 largest regular files, logical bytes and relative paths.
TAR-LOG.txt: archiver diagnostics; live sockets are not normal stored files.

Upload ALL .part-* files plus SHA256SUMS.txt, READ-ME.txt,
DIRECTORY-SIZES.txt, LARGEST-FILES.tsv, SYMLINKS.tsv and TAR-LOG.txt.
Only consider the capture ready when VERIFIED.txt exists and FAILED.txt does not.

To verify after downloading all parts into one directory:
  sha256sum -c SHA256SUMS.txt

To reconstruct the original compressed tar (needs additional disk space):
  cat -- neuron-v16.2.tar.gz.part-* > neuron-v16.2.tar.gz

To extract directly into a NEW empty review directory instead:
  mkdir neuron-review-extracted
  cat -- neuron-v16.2.tar.gz.part-* | tar -xzf - -C neuron-review-extracted
EOF

printf 'Source: %s\nOutput: %s\nPart limit: %s bytes\n' "$PROJECT" "$OUT" "$PART_BYTES"
printf '\nRecording directory sizes and largest files...\n'
df -h -- "$PROJECT" "$OUT" > "$OUT/DISK-SPACE.txt"
du -h --max-depth=2 -- "$PROJECT" | sort -hr > "$OUT/DIRECTORY-SIZES.txt"
find "$PROJECT" -type f -printf '%s\t%P\n' | sort -nr | sed -n '1,150p' > "$OUT/LARGEST-FILES.tsv"
find "$PROJECT" -type l -printf '%P\t%l\n' > "$OUT/SYMLINKS.tsv"

printf 'Streaming the full project into compressed parts; no intermediate copy...\n'
tar --sparse -C "$SOURCE_PARENT" -cf - -- "$SOURCE_NAME" 2> "$OUT/TAR-LOG.txt" \
    | gzip -1 \
    | split --bytes="$PART_BYTES" --numeric-suffixes=0 --suffix-length=4 - "$OUT/$PREFIX"

shopt -s nullglob
parts=("$OUT"/"$PREFIX"*)
(( ${#parts[@]} > 0 )) || fail 'No archive parts were produced.'
for part in "${parts[@]}"; do
    bytes="$(stat -c %s -- "$part")"
    (( bytes > 0 && bytes <= PART_BYTES )) || fail "Invalid part size: $part ($bytes bytes)"
done

printf 'Checking the compressed stream and tar structure...\n'
cat -- "${parts[@]}" | gzip -t
cat -- "${parts[@]}" | tar -tzf - > /dev/null
printf 'Writing checksums...\n'
(
    cd "$OUT"
    sha256sum -- "${PREFIX}"* READ-ME.txt DIRECTORY-SIZES.txt LARGEST-FILES.tsv SYMLINKS.tsv TAR-LOG.txt DISK-SPACE.txt > SHA256SUMS.txt
    sha256sum -c SHA256SUMS.txt > CHECKSUM-VERIFICATION.txt
)
printf 'VERIFIED UTC: %s\nParts: %s\nMaximum part bytes: %s\nGzip integrity: PASS\nTar structure: PASS\nChecksums: PASS\nLive database consistency: NOT ASSERTED\n' \
    "$(date -u +%FT%TZ)" "${#parts[@]}" "$PART_BYTES" > "$OUT/VERIFIED.txt"

printf '\nSUCCESS: %s archive part(s), each at most %s bytes.\n' "${#parts[@]}" "$PART_BYTES"
printf 'Upload the parts and reports from this folder:\n%s\n\n' "$OUT"
printf 'Largest directories:\n'
sed -n '1,15p' "$OUT/DIRECTORY-SIZES.txt"
