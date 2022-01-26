#!/usr/bin/bash


if [ "0" == "$#" ]; then
	echo "pass in a markdown file to export"
	exit
fi

# set infile_bname (basename $infile)
# set split_f (string split . $infile_bname)
# set out_name "$DT/$split_f[1]"

IN_FILE="$1"
IN_FILE_BNAME=$(basename $IN_FILE)
FNAME="${IN_FILE_BNAME%.*}"
OUT_FILE="$DT/$FNAME.pdf"

echo "exporting $IN_FILE to $OUT_FILE"

cat ~/.config/fish/functions/md_font_header.md > /tmp/mdpdfdt.tmp
cat $IN_FILE >> /tmp/mdpdfdt.tmp

# pandoc $infile -f gfm -o $out_name.html --pdf-engine=wkhtmltopdf  --metadata pagetitle="$out_name" 
# pandoc $infile -f gfm -o $out_name.pdf --pdf-engine=wkhtmltopdf  --metadata pagetitle="$out_name" 
# pandoc $infile -f gfm -o $out_name.pdf --pdf-engine=pdflatex
# pandoc /tmp/mdpdfdt.tmp -f markdown -o $out_name.pdf --pdf-engine=wkhtmltopdf  --metadata pagetitle="$out_name" --katex=$HOME/Projects/katex
# pandoc /tmp/mdpdfdt.tmp -f gfm -o $out_name.pdf --pdf-engine=wkhtmltopdf  --metadata pagetitle="$out_name" 
# pandoc /tmp/mdpdfdt.tmp -f gfm -o $out_name.pdf --pdf-engine=pdflatex  --metadata pagetitle="$out_name" 
pandoc /tmp/mdpdfdt.tmp -f markdown -o $OUT_FILE --pdf-engine=wkhtmltopdf --metadata pagetitle="$out_name" --katex=https://cdn.jsdelivr.net/npm/katex@0.15.1/dist/

