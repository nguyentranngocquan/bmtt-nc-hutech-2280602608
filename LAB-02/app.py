from flask import Flask, render_template, request
from cipher.caesar import CaesarCipher

app = Flask(__name__)

# Route trang chủ
@app.route("/")
def home():
    return render_template('index.html')

# Route trang Caesar Cipher
@app.route("/caesar")
def caesar():
    return render_template('caesar.html')
 
# Route mã hóa Caesar
@app.route("/encrypt", methods=['POST'])
def caesar_encrypt():
    text = request.form['inputPlainText']
    key = int(request.form['inputKeyPlain'])
    caesar = CaesarCipher()
    encrypted_text = caesar.encrypt(text, key)
    return f"Text: {text}<br>Key: {key}<br>Encrypted text: {encrypted_text}"

# Route giải mã Caesar
@app.route("/decrypt", methods=['POST'])
def caesar_decrypt():
    text = request.form['inputCipherText']
    key = int(request.form['inputKeyCipher'])
    caesar = CaesarCipher()
    decrypted_text = caesar.decrypt(text, key)
    return f"Text: {text}<br>Key: {key}<br>Decrypted text: {decrypted_text}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)
