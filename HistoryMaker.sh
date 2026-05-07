#!/bin/bash

OUTPUT="LOGBOOKs.md"

echo "# 📒 Project Development Logbook" > "$OUTPUT"
echo "" >> "$OUTPUT"

# Temporary file
TMP=$(mktemp)

# Save commits safely
git log --reverse --format='%H' > "$TMP"

while read -r hash
do
    date=$(git show -s --format='%ad' \
        --date=format:'%a %b %d, %Y %H:%M:%S' "$hash")

    msg=$(git show -s --format='%B' "$hash")

    day=$(echo "$date" | cut -d',' -f1)
    time=$(echo "$date" | awk '{print $4}')

    {
        echo "## 📅 $day"
        echo ""

        echo "### 🕒 $time"
        echo ""

        echo "#### 📝 Commit Message"
        echo '```text'
        echo "$msg"
        echo '```'
        echo ""

        echo "#### 🛠 Changes"
        echo '```text'
        git show --stat --pretty=format:"" "$hash"
        echo '```'
        echo ""

    } >> "$OUTPUT"

done < "$TMP"

rm "$TMP"

echo "✅ Logbook generated: $OUTPUT"
