
URL=http://hg.tobiasussing.dk/hgweb.cgi/youtubexbmc/
DIRNAME=plugin.video.youtube
RELEASEPATH=/usr/local/www/data/hg/nightly-repo/
BETAVERSION=3.4.0
RELEASEVERSION=3.3.0

echo "PID: $$"

# Check if trigger is set
if [ -f release ]; then
    echo "Found release";
    rm release;
else
    echo "Not set to release";
    exit;
fi

cd /tmp

TMPDIR="/tmp/release-tmp-$$"
mkdir $TMPDIR
cd $TMPDIR

OWD=`pwd`
echo "OWD: $OWD"

mkdir trunk
hg clone $URL trunk/$DIRNAME

hg clone $URL $DIRNAME -b release

echo "WORKING DIR $OWD DOING $DIRNAME"
cd $OWD/$DIRNAME;
hg update release;
cp -R $OWD/trunk/$DIRNAME/plugin/* $OWD/$DIRNAME/;
rm -fv *pyc */*pyc */*/*pyc  *~ */*~ */*/*~
#hg add * */* */*/*;
#hg add *
for j in `ls $OWD/$DIRNAME/ | egrep "addon.xml"`; do
   echo "Cleaning addon.xml $j";
   cat $OWD/trunk/$DIRNAME/plugin/$j | sed -e 's/.beta//' | sed -e 's/ Beta//' | sed -e 's/.999/.0/'> $OWD/$DIRNAME/$j;
done;
VERSION=`cat $OWD/$DIRNAME/addon.xml |grep "addon id" |awk -F\'  ' { print $4 } '`;
CVERSION=`cat $OWD/$DIRNAME/default.py $OWD/$DIRNAME/lib/*.py |grep "version =" |awk -F\"  ' { print $2 } '`;
if [ "$VERSION" != "$CVERSION" ]; then
  echo "ERROR version mismatch on $DIRNAME";
  echo "$DIRNAME version $VERSION - $CVERSION";
  exit
fi;
if [ "$VERSION" = "$CVERSION" ]; then
   echo "Removing beta tags";
   for j in `ls $OWD/$DIRNAME/ | egrep ".py"`; do
          echo "Cleaning .py $j";
             cat $OWD/trunk/$DIRNAME/plugin/$j | sed -e 's/.beta//' | sed -e 's/ Beta//' > $OWD/$DIRNAME/$j;
   done;
   for j in `ls $OWD/$DIRNAME/lib/ | grep ".py"`; do
          echo "Cleaning lib .py $j";
             cat $OWD/trunk/$DIRNAME/plugin/lib/$j | sed -e 's/.beta//' | sed -e 's/ Beta//' > $OWD/$DIRNAME/lib/$j;
   done;
fi;

echo "Push updates to relese branch"
cd $OWD/$DIRNAME/
hg add && hg commit -m "Release script commit" && hg push || echo "Nothing to commit"

if [ -d $RELEASEPATH ]; then
    # Make zip file
    cd $OWD;
    zip -r $DIRNAME-$VERSION.zip $DIRNAME/ -x *.pyc */*.hg/*
    mv $DIRNAME-$VERSION.zip $RELEASEPATH/$DIRNAME/
    cp $DIRNAME/changelog.txt $RELEASEPATH/$DIRNAME/changelog-$VERSION.txt
    if [ -f $DIRNAME/icon.png ]; then
        cp $DIRNAME/icon.png $RELEASEPATH/$DIRNAME/;
    fi
fi

rm -fr $TMPDIR

######
if [ -d $RELEASEPATH ]; then
    cd $RELEASEPATH 
    cp tmp/$DIRNAME/addon.xml addons/$DIRNAME-release.xml

    echo "<?xml version='1.0' encoding='UTF-8'?><addons>" > addons-temp.xml
    cat addons/* >> addons-temp.xml
    echo "</addons>" >> addons-temp.xml
    sed -e "s/<?xml version='1.0' encoding='UTF-8' standalone='yes'?>//g" addons-temp.xml | sed -e 's/<?xml version="1.0" encoding="UTF-8" standalone="yes"?>//g' > addons.xml
    rm addons-temp.xml
    md5 -r addons.xml > addons.xml.md5
fi
