import phonenumbers
from phonenumbers import geocoder, carrier, timezone

def lookup_number(number):
    try:
        # Si numéro commence par 0, on ajoute l'indicatif français automatiquement
        if number.startswith("0"):
            number = "+33" + number[1:]

        parsed = phonenumbers.parse(number)

        if not phonenumbers.is_valid_number(parsed):
            print("❌ Numéro invalide.")
            return

        print(f"\n📞 Numéro : {number}")
        print(f"🌍 Région : {geocoder.description_for_number(parsed, 'fr')}")
        print(f"🏢 Opérateur : {carrier.name_for_number(parsed, 'fr')}")
        print(f"🕓 Fuseaux horaires : {', '.join(timezone.time_zones_for_number(parsed))}")

    except Exception as e:
        print(f"❌ Erreur : {e}")

if __name__ == "__main__":
    number = input("📱 Entrez un numéro (ex: 06... ou +336...) puis appuyez sur Entrée : ").strip()

    if number:
        lookup_number(number)
    else:
        print("❌ Aucun numéro entré.")

    # Attente d'une touche pour revenir automatiquement au menu
    input("\n🔁 Appuyez sur Entrée pour revenir au menu...")
