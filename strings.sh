#!/bin/sh
od -c /Volumes/RAMDisk/mem  | cut -c 1-8,16,24,32,40,48,56,64,72
