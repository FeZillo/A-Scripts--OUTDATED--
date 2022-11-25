import amino, threading, tqdm, time, pyfiglet, colorama
from amino import ACM
from colorama import Fore, Style
from tqdm import tqdm
client = amino.Client()

contador = 0

cores = {
    "b": "\033[1;107;30m",
    "r": "\033[1;104m",
    "m": "\033[1;97m"
}
ll = pyfiglet.figlet_format
print(f"{cores['b']}")
print("                        ❖ Massive Transfer ❖                            ")
print(f"{cores['r']}")
print(Fore.WHITE)
print(f"✠ By {cores['b']} Sophyy(FeZillo) ✠ ")
print(f"{cores['r']}")
print(Fore.WHITE)
print("")
print(f"{cores['b']}           ❖ LOGIN ❖            {cores['r']}", Fore.WHITE)
e = ("your_email")
p = ("your_password")
link = input("Coloque o link do perfil >> ")
client.login(e, p)
print("")
print(f"{cores['b']}           ❖ INFORMAÇÕES ❖            {cores['r']}")
print(f"{cores['r']}")
print(Fore.WHITE)
comId = client.get_from_code(link).comId
client.join_community(comId)
userId = client.get_from_code(link).objectId
coins = int(client.get_wallet_info().totalCoins)
nick = client.get_user_info(userId).nickname
print(f"Seus coins: {cores['b']} {coins} {cores['r']}", Fore.WHITE)
print(f"Nome do destinario: {nick}")
print("")
print(f"{cores['b']}           ❖ COLOCANDO VIP ❖            {cores['r']}", Fore.WHITE)
profile = client.get_user_info(userId).UserProfile
acm = ACM(comId=comId, profile=profile)
try:
	acm.add_influencer(userId=userId, monthlyFee=500)
except Exception as j:
	print(j)
	pass
	
print("VIP COLOCADO COM SUCESSO!!")
print("")
print(f"{cores['b']}           ❖ TRANSFERENCIA ❖            {cores['r']}", Fore.WHITE)

c = int(input("Quantos coins quer enviar >> "))
print()
ck = coins - c
sb = amino.SubClient(profile = client.profile, comId = comId)
for i in tqdm(range(c // 500)):
        time.sleep(0.03)
        threading.Thread(target=sb.subscribe, args=(userId, )).start()

            
time.sleep(5)
check = int(client.get_wallet_info().totalCoins) - ck

print(f"Faltam:  {cores['b']} {check} {cores['r']}", Fore.WHITE)
if check > 0:
	print("CORRIGINDO!!!")


if check > 0:
    try:
        for i in tqdm(range(check // 500)):
            time.sleep(0.4)
            threading.Thread(target=sb.subscribe, args=(userId, )).start()
    except Exception as j:
        print(j)
        
        

sb.start_chat(userId = userId, message = (f"[B]🌟 Você acaba de receber {c} coins, verifique sua carteira 🌟"))
time.sleep(2)
coinsp = client.get_wallet_info().totalCoins
print(f"Seus Coins atuais: {cores['b']} {coinsp} {cores['r']}", Fore.WHITE)
print("")
print(f"{cores['b']}           ❖ RETIRANDO VIP ❖            {cores['r']}", Fore.WHITE)
acm.remove_influencer(userId=userId)
print("VIP RETIRADO COM SUCESSO!!")