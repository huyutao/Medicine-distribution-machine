from subprocess import *
import cognitive_face as CF

KEY = '81141d94e79246b9b5743e18ec7db7c4'
CF.Key.set(KEY)

Controller_path = "/Users/luris/VendingMachine_Control"

Doctor_server = "mingxuanhe@192.168.1.130"
Doctor_path = "/Users/mingxuanhe/Desktop/Hacks"

Raspberry_server = "pi@192.168.1.133"
Raspberry_path = "/home/pi"

input_photo = "image.jpg"
request_photo = "face.jpg"
request_file = "request"
medicine_file = "medicines"

Raspberry_initial = "python " + Raspberry_path + "/script/main_loop.py"
Raspberry_get = "scp " + Raspberry_server + ":" + Raspberry_path + "/" + input_photo + " " + Controller_path
Doctor_get_request = "scp " + Doctor_server + ":" + Doctor_path + "/Temp/" + request_file + " " + Controller_path


def send_command(server, command):

    result = check_output(["ssh", server, command])

    return result


def get_request_image(user_id):

    doctor_get_image = "scp " + Doctor_server + ":" + Doctor_path + "/Data/" + user_id + "/" + request_photo + " " + Controller_path
    check_call(doctor_get_image.split(" "))


def get_request_medicine(user_id):

    doctor_get_medicine = "scp " + Doctor_server + ":" + Doctor_path + "/Data/" + user_id + "/" + medicine_file + " " + Controller_path
    check_call(doctor_get_medicine.split(" "))


def send_out_medicine():

    with open(medicine_file, "r") as med_list:
        for item in med_list:
            command = "python " + Raspberry_path + "/script/m" + str(item).strip() + ".py"
            send_command(Raspberry_server, command)
            print command


def compare_images(image1, image2):
    face_id_1 = CF.face.detect(image1)[0]['faceId']
    face_id_2 = CF.face.detect(image2)[0]['faceId']

    result = CF.face.verify(face_id_1, face_id_2)

    return result['isIdentical']


def main():
    # Start Raspberry initialization
    success = send_command(Raspberry_server, Raspberry_initial)

    # If photo capture success, get the photo from raspberry
    if success:
        check_call(Raspberry_get.split(" "))

    remain_request = []
    check_call(Doctor_get_request.split(" "))
    with open(request_file, "r") as request_list:
        # For every request still in request file
        for request in request_list:

            user_id = str(request).strip()

            # Get the image from doctor server
            get_request_image(user_id)

            if compare_images(request_photo, input_photo):

                get_request_medicine(user_id)
                send_out_medicine()

            else:
                remain_request.append(user_id)

        print remain_request
        #update_request(remin_request)


if __name__ == "__main__":
    main()
