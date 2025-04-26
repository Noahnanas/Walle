#include <Elegoo_GFX.h>
#include <Elegoo_TFTLCD.h>
#include <SD.h>
#include <SPI.h>

#define LCD_CS A3
#define LCD_CD A2
#define LCD_WR A1
#define LCD_RD A0
#define LCD_RESET A4
#define PIN_SD_CS 10

Elegoo_TFTLCD tft(LCD_CS, LCD_CD, LCD_WR, LCD_RD, LCD_RESET);

#define BLACK   0x0000
#define BLUE    0x001F
#define RED     0xF800
#define GREEN   0x07E0
#define CYAN    0x07FF
#define MAGENTA 0xF81F
#define YELLOW  0xFFE0
#define WHITE   0xFFFF

const int __Gnbmp_height = 320;
const int __Gnbmp_width  = 240;
unsigned char __Gnbmp_image_offset  = 0;
File bmpFile;

#define BUFFPIXEL       60
#define BUFFPIXEL_X3    180

void bmpdraw(File f, int x, int y) {
  bmpFile.seek(__Gnbmp_image_offset);
  uint8_t sdbuffer[BUFFPIXEL_X3];

  for (int i = __Gnbmp_height - 1; i >= 0; i--) {
    for (int j = 0; j < (240 / BUFFPIXEL); j++) {
      bmpFile.read(sdbuffer, BUFFPIXEL_X3);

      uint8_t buffidx = 0;
      int offset_x = j * BUFFPIXEL;
      unsigned int __color[BUFFPIXEL];

      for (int k = 0; k < BUFFPIXEL; k++) {
        __color[k] = sdbuffer[buffidx + 2] >> 3;
        __color[k] = __color[k] << 6 | (sdbuffer[buffidx + 1] >> 2);
        __color[k] = __color[k] << 5 | (sdbuffer[buffidx + 0] >> 3);
        buffidx += 3;
      }

      for (int m = 0; m < BUFFPIXEL; m++) {
        tft.drawPixel(m + offset_x, i, __color[m]);
      }
    }
  }
}

boolean bmpReadHeader(File f) {
  uint32_t tmp;
  uint8_t bmpDepth;

  if (read16(f) != 0x4D42) return false;

  tmp = read32(f);
  read32(f);
  __Gnbmp_image_offset = read32(f);
  tmp = read32(f);

  int bmp_width = read32(f);
  int bmp_height = read32(f);
  if (bmp_width != __Gnbmp_width || bmp_height != __Gnbmp_height) return false;

  if (read16(f) != 1) return false;

  bmpDepth = read16(f);
  if (read32(f) != 0) return false;

  return true;
}

uint16_t read16(File f) {
  uint16_t d;
  uint8_t b;
  b = f.read();
  d = f.read();
  d <<= 8;
  d |= b;
  return d;
}

uint32_t read32(File f) {
  uint32_t d;
  uint16_t b;

  b = read16(f);
  d = read16(f);
  d <<= 16;
  d |= b;
  return d;
}

void setup(void) {
  Serial.begin(9600);
  tft.reset();

  uint16_t identifier = tft.readID();
  if (identifier == 0x0101) {
    identifier = 0x9341;
  }

  tft.begin(identifier);
  tft.fillScreen(BLUE);

  pinMode(10, OUTPUT);
  if (!SD.begin(10)) {
    Serial.println("SD init failed");
    tft.setCursor(0, 0);
    tft.setTextColor(WHITE);    
    tft.setTextSize(1);
    tft.println("SD Card Init fail.");   
  } else {
    Serial.println("SD init done.");
  }
}

void loop(void) {
  int raw = analogRead(A5); // ← À adapter si tu utilises un autre pin
  float voltage = raw * (5.0 / 1023.0); // ajuster si diviseur de tension

  int batteryPercent = constrain(map(voltage * 100, 300, 420, 0, 100), 0, 100);
  batteryPercent = (batteryPercent / 10) * 10;

  char filename[20];
  sprintf(filename, "CHARGE%02d.BMP", batteryPercent);

  Serial.print("Battery: ");
  Serial.print(batteryPercent);
  Serial.print("% => ");
  Serial.println(filename);

  bmpFile = SD.open(filename);
  if (!bmpFile) {
    Serial.println("BMP file not found");
    return;
  }

  if (!bmpReadHeader(bmpFile)) {
    Serial.println("Invalid BMP header");
    bmpFile.close();
    return;
  }

  bmpdraw(bmpFile, 0, 0);
  bmpFile.close();

  delay(100);
}