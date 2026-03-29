import asyncio
from datetime import datetime


def log(func):
    def wrapper(self,mesaj):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] LOG: '{self.ad}' mesaj gönderdi → '{mesaj}'")
        return func(self,mesaj)
    return wrapper

class ChatLog:
    def __init__(self):
        self.kayit = []

    def ekle(self,kullanici,mesaj,yanit):
        self.kayit.append({
            "kullanici":kullanici,
            "mesaj":mesaj,
            "yanit":yanit,
            "tarih":datetime.now().strftime('%H:%M:%S')
        })

    def goster(self):
        for i,kayit in enumerate(self.kayit,1):
            print(f"{i}. [{kayit['tarih']}] {kayit['kullanici']}: {kayit['mesaj']} → {kayit['yanit']}")

    def filtrele(self, kelime):
        bulundu = False
        for kayit in self.kayit:
            if kelime.lower() in kayit["mesaj"].lower():
                print(f"{kayit['kullanici']}: {kayit['mesaj']}")
                bulundu = True

        if not bulundu:
            print("Aranan kelime bulunamadı.")


class Ai:
    def __init__(self,ad):
        self.ad = ad

    @log
    async def yanit_ver(self,mesaj):
        await asyncio.sleep(1)
        if "iade" in mesaj.lower():
            return "İade talebiniz alınmıştır."
        elif "kargo" in mesaj.lower():
            return "Kargo süreciniz kontrol ediliyor."
        else:
            return "Talebiniz işleme alındı."


class Kullanici:
    def __init__(self,ad,rol,model,log_defteri):
        self.ad = ad
        self.model = model
        self.log_defteri = log_defteri
        self.rol = rol

        if self.rol == "admin":
            print("Admin Kullanıcı")

    @log
    async def mesaj_gonder(self,mesaj):
        yanit = await self.model.yanit_ver(mesaj)
        self.log_defteri.ekle(self.ad,mesaj,yanit)
        print(f"AI Yanıtı: {yanit}")
        if len(mesaj) > 50:
            print("Uzun mesaj gönderildi")
        else:
            print("Kısa mesaj")
        return yanit


puan_hesapla = lambda mesaj:len(mesaj) * 0.75

# Nesneleri oluştur
model = Ai("AsistanBot")
chatlog = ChatLog()
kullanici = Kullanici("boratopcu37","admin" ,model, chatlog)

#Konuşma Senaryosu
async def main():
    await kullanici.mesaj_gonder("Merhaba, iadem işleme alındı mı?")
    await kullanici.mesaj_gonder("Kargom hala gelmedi, yardımcı olur musunuz?")

    chatlog.goster()

    print("\n--- Performans Analizi ---")
    for kayit in chatlog.kayit:
        puan = puan_hesapla(kayit["mesaj"])
        print(f"Yanıt: '{kayit['yanit'][:30]}...' → Puan: {puan:.2f}")


if __name__ == "__main__":
    asyncio.run(main())
