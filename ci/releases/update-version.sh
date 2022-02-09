#!/bin/bash
###########################
# frigate Version Updater #
###########################

## Usage
# bash update-version.sh <new_version>

set -e

# Format is YY.MM.PP - no leading 'v' or trailing 'a'
NEXT_FULL_TAG=$1

# Get current version
CURRENT_TAG=$(git tag --merged HEAD | grep -xE '^v.*' | sort --version-sort | tail -n 1 | tr -d 'v')
CURRENT_MAJOR=$(echo $CURRENT_TAG | awk '{split($0, a, "."); print a[1]}')
CURRENT_MINOR=$(echo $CURRENT_TAG | awk '{split($0, a, "."); print a[2]}')
CURRENT_PATCH=$(echo $CURRENT_TAG | awk '{split($0, a, "."); print a[3]}')
CURRENT_SHORT_TAG=${CURRENT_MAJOR}.${CURRENT_MINOR}

#Get <major>.<minor> for next version
NEXT_MAJOR=$(echo $NEXT_FULL_TAG | awk '{split($0, a, "."); print a[1]}')
NEXT_MINOR=$(echo $NEXT_FULL_TAG | awk '{split($0, a, "."); print a[2]}')
NEXT_SHORT_TAG=${NEXT_MAJOR}.${NEXT_MINOR}

echo "Preparing release $CURRENT_TAG => $NEXT_FULL_TAG"

# Determine release type
if [ "$RELEASE_TYPE" == "major" ]; then
  NEXT_FULL_TAG="${NEXT_MAJOR}.0.0"
  NEXT_SHORT_TAG="${NEXT_MAJOR}.0"
elif [ "$RELEASE_TYPE" == "minor" ]; then
  NEXT_FULL_TAG="${CURRENT_MAJOR}.${NEXT_MINOR}.0"
  NEXT_SHORT_TAG="${CURRENT_MAJOR}.${NEXT_MINOR}"
elif [ "$RELEASE_TYPE" == "patch" ]; then
  NEXT_FULL_TAG="${CURRENT_MAJOR}.${CURRENT_MINOR}.${NEXT_PATCH}"
  NEXT_SHORT_TAG="${CURRENT_MAJOR}.${CURRENT_MINOR}"
else
  echo "Incorrect release type; use 'major', 'minor', or 'patch' as an argument"
  exit 1
fi

echo "Preparing '$RELEASE_TYPE' release [$CURRENT_TAG -> $NEXT_FULL_TAG]"

# Inplace sed replace; workaround for Linux and Mac
function sed_runner() {
    sed -i.bak ''"$1"'' $2 && rm -f ${2}.bak
}

# No-op