#include <Elegoo_GFX.h>
#include <Elegoo_TFTLCD.h>
#include "woof.h"  // Ton image convertie

#define LCD_CS A3
#define LCD_CD A2
#define LCD_WR A1
#define LCD_RD A0
#define LCD_RESET A4

Elegoo_TFTLCD tft(LCD_CS, LCD_CD, LCD_WR, LCD_RD, LCD_RESET);

void setup() {
  Serial.begin(9600);
  tft.reset();

  uint16_t identifier = tft.readID();
  if (identifier == 0x0101) identifier = 0x9341; // fallback

  tft.begin(identifier);
  tft.setRotation(1);  // Orientation paysage
  tft.fillScreen(0x0000); // Noir

  // Affichage de l'image pixel par pixel
  for (int16_t y = 0; y < WOOF_HEIGHT; y++) {
    for (int16_t x = 0; x < WOOF_WIDTH; x++) {
      uint16_t color = pgm_read_word(&woof[y * WOOF_WIDTH + x]);
      tft.drawPixel(x, y, color);
    }
  }
}

void loop() {
  // Rien ici pour l’instant
}
