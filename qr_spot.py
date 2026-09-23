import qrcode
img = qrcode.make('https://spotweb.pythonanywhere.com/menu')
img.save('qr_spot.png')