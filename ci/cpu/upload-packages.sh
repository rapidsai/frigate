#!/bin/bash
# Copyright (c) 2018, NVIDIA CORPORATION.

if [[ "${BUILD_MODE}" != "branch" ]]; then
  echo "Skipping upload"
  return 0
fi

if [ -z "$MY_UPLOAD_KEY" ]; then
  echo "No upload key"
  return 0
fi

if [ -z "$TWINE_PASSWORD" ]; then
  echo "TWINE_PASSWORD not set"
  return 0
fi

anaconda -t ${MY_UPLOAD_KEY} upload -u ${CONDA_USERNAME:-rapidsai} --label main --skip-existing "`conda build conda/recipes/frigate --output`" --no-progress

echo "Upload pypi"
twine upload --skip-existing -u ${TWINE_USERNAME:-rapidsai} dist/*
