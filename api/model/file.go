package model

import (
	validation "github.com/go-ozzo/ozzo-validation"
)

//File model
type File struct {
	BaseModel
	Type   string `json:"type"`
	UserID int    `json:"user_id"`
	URL    string `json:"url"`
}

//Validate for user model
func (f File) Validate() error {
	return validation.ValidateStruct(&f,
		validation.Field(&f.Type, validation.Required),
		validation.Field(&f.UserID, validation.Required),
		validation.Field(&f.URL, validation.Required),
	)
}
