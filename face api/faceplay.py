import cognitive_face as CF

KEY = '81141d94e79246b9b5743e18ec7db7c4'
CF.Key.set(KEY)

img_url = 'https://raw.githubusercontent.com/Microsoft/Cognitive-Face-Windows/master/Data/detection1.jpg'
result = CF.face.detect(img_url)
print result
