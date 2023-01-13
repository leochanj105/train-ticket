#!/usr/bin/env bash
set -eux

echo
echo "Publishing images, Repo: $1, Tag: $2"
echo
for dir in ts-*; do
    if [[ -d $dir ]]; then
        if [[ -n $(ls "$dir" | grep -i Dockerfile) ]]; then
            echo "publish ${dir}"
	    # Must use `buildx` as docker build tool
            # docker build --push -t "$1"/"${dir}":"$2" "$dir"
            docker push "$1"/"${dir}":"$2"
        fi
    fi
done
