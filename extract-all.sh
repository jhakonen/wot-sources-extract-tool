#!/bin/bash
WOTPATH=$(wot-dir)

SCRIPTDIR=$(dirname "$(readlink -f "$0")")
OUTPATH=$SCRIPTDIR/extracts

echo Removing "$OUTPATH/py"
rm -r "$OUTPATH/py"
echo Removing "$OUTPATH/as"
rm -r "$OUTPATH/as"

(cd docker; docker build -t jhakonen/wot-sources .)
(cd docker; docker run --rm -it -v $WOTPATH:/input -v $OUTPATH:/output jhakonen/wot-sources)
