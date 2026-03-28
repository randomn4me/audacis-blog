HEIC_FILES := $(wildcard static/img/*.heic static/img/*.HEIC)
JPG_FROM_HEIC := $(patsubst %.heic,%.jpg,$(patsubst %.HEIC,%.jpg,$(HEIC_FILES)))

%.jpg: %.heic
	sips -s format jpeg -s formatOptions 90 "$<" --out "$@"

%.jpg: %.HEIC
	sips -s format jpeg -s formatOptions 90 "$<" --out "$@"

.PHONY: convert build serve clean

convert: $(JPG_FROM_HEIC)

build: convert
	zola build

serve: convert
	zola serve

clean:
	rm -f $(JPG_FROM_HEIC)
