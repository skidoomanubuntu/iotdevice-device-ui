#!/bin/bash
cd $SNAP
$SNAP/bin/uvicorn app.main:app --port 4501 --host 0.0.0.0
