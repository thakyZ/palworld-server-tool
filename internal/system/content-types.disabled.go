package system

import (
	"path"
)

const (
	ContentTypeJSON       = "application/json"
	ContentTypeXML        = "application/xml"
	ContentTypeHTML       = "text/html"
	ContentTypePlain      = "text/plain"
	ContentTypePDF        = "application/pdf"
	ContentTypeCSS        = "text/css"
	ContentTypeJavaScript = "application/javascript"
	ContentTypeSVG        = "image/svg+xml"
	ContentTypeGIF        = "image/gif"
	ContentTypeBMP        = "image/bmp"
	ContentTypeICO        = "image/x-icon"
	ContentTypeMP4        = "video/mp4"
	ContentTypeMP3        = "audio/mpeg"
	ContentTypeJPG        = "image/jpeg"
	ContentTypePNG        = "image/png"
	ContentTypeFontOpen   = "font/opentype"
	ContentTypeOctet      = "application/octet-stream"
)

func GetContentTypeByFileExtension(filename string) string {
	switch path.Ext(filename) {
	case ".css":
		return ContentTypeCSS
	case ".js":
		return ContentTypeJavaScript
	case ".png":
		return ContentTypePNG
	case ".jpg", ".jpeg":
		return ContentTypeJPG
	case ".svg":
		return ContentTypeSVG
	default:
		return ContentTypeOctet
	}
}