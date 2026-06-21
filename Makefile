HEIC_FILES := $(wildcard img_src/*.heic img_src/*.HEIC)
JPG_FROM_HEIC := $(patsubst %.heic,%.jpg,$(patsubst %.HEIC,%.jpg,$(HEIC_FILES)))

# Convert camera HEIC to a downsized, metadata-stripped JPG. img_src/ is the
# image source dir; it is never served. resize_image generates the served
# webp/jpg variants at build time.
%.jpg: %.heic
	sips -s format jpeg -s formatOptions 90 -Z 1920 "$<" --out "$@"
	exiftool -all= -overwrite_original "$@"

%.jpg: %.HEIC
	sips -s format jpeg -s formatOptions 90 -Z 1920 "$<" --out "$@"
	exiftool -all= -overwrite_original "$@"

.PHONY: convert build serve clean

convert: $(JPG_FROM_HEIC)

build: convert
	zola build

serve: convert
	zola serve

clean:
	rm -f $(JPG_FROM_HEIC)
