import VKapi
import YandexAPI

access_token_vk = 'vk1.a.RQ0L9ImzVUBLnJ0jvDsnMgW1EjZlyBGHghvBXiBKpXtkYctv4X_UJBTnvasVrDGrsl1lPQrIAP-budDn4RsPYS2XhvrHwp8pgtoDmCxIizRHVuaXeEf-UoImbAwBr3mlMl_z5JkjPdvruCUyFO51GK8dU2KPvUKA0CQ16cppnhvA3Lvo7nJ_rX0V12cJ8j224LOiUJT1NoMmoha7ommtWA'
vk = VKapi.VK(access_token_vk)
yandex = YandexAPI.YandexDisk()

while True:
    print("This program save your VK photos to Yandex disk")
    if vk.id == "":
        user_id = input("enter your vk id: ")
        vk.change_id(user_id)
    if yandex.yandex_token == "":
        yandex_token = input("enter your yandex disk token: ")
        yandex.change_token(yandex_token)
    while True:
        print("Select option:\n1.Save photos from VK\n2.Load photos to Yandex disk\n"
              "3.Change user id\n4.Change Yandex disk token\n5.Exit\n")
        selected_option = input()
        if selected_option == "1":
            album = input("Choose album\n1.profile\n2.wall\n")
            if album == '1':
                vk.save_photos('profile')
            elif album == '2':
                vk.save_photos('wall')
            else:
                print("No such option")
        elif selected_option == "2":
            if not vk.photos_info['photos']:
                vk.save_photos('profile')
            yandex.send_photo_yandex(input("enter folder name\n"), vk.photos_info, int(input("enter the number of photos\n")))
        elif selected_option == "3":
            vk.change_id(input("enter new vk id"))
        elif selected_option == "4":
            yandex.change_token(input("enter new Yandex disk token"))
        elif selected_option == "5":
            quit()
        else:
            print("No such option")
