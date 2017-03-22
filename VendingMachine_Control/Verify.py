from subprocess import *
import cognitive_face as CF

KEY = '81141d94e79246b9b5743e18ec7db7c4'
CF.Key.set(KEY)

Controller_path = "/home/yutao/PycharmProjects/archhack/VendingMachine_Control"

Doctor_path = "/home/yutao/PycharmProjects/archhack/doctor"

Raspberry_server = "pi@172.20.10.12"
Raspberry_path = "/home/pi"

input_photo = "image.jpg"
request_photo = "face.jpg"
request_file = "request"
medicine_file = "medicines"

Raspberry_initial = "python " + Raspberry_path + "/script/main_loop.py"
Raspberry_get = "scp " + Raspberry_server + ":" + Raspberry_path + "/pi/" + input_photo + " " + Controller_path
update_doctor_request = "cp " + Controller_path + "/" + request_file + " " + Doctor_path + "/Temp"


def send_command(server, command):

    result = check_output(["ssh", server, command])

    return result


def get_request_image(user_id):

    doctor_get_image = "cp " + Doctor_path + "/Data/" \
                       + user_id + "/" + request_photo + " " + Controller_path
    check_call(doctor_get_image.split(" "))


def transfer_request_medicine(user_id):

    # doctor_get_medicine = "cp " + Doctor_path + "/Data/" + user_id + "/" + medicine_file + " " + Controller_path
    send_medicine = "scp " + Doctor_path + "/Data/" + user_id + "/" + medicine_file + " " + Raspberry_server + ":" + Raspberry_path + "/script"
    # check_call(doctor_get_medicine.split(" "))
    check_call(send_medicine.split(" "))


def compare_images(image1, image2):

    print
    try:
        face_id_1 = CF.face.detect(image1)[0]['faceId']
        face_id_2 = CF.face.detect(image2)[0]['faceId']

        result = CF.face.verify(face_id_1, face_id_2)['isIdentical']

    except:
        result = False

    return result


def update_request(remain_request):

    with open(request_file, 'w') as new_request:
        for item in remain_request:
            new_request.write(str(item) + '\n')
    check_call(update_doctor_request.split(" "))


def main():
    # Start Raspberry initialization
    # success = send_command(Raspberry_server, Raspberry_initial)

    # get the photo from raspberry

    match_found = False
    remain_request = []
    #check_call(Raspberry_get.split(" "))
    #check_call(Doctor_get_request.split(" "))

    temp_id = ""
    with open(Doctor_path + "/Temp/" + request_file, "r") as request_list:
        # For every request still in request file
        for request in request_list:

            user_id = str(request).strip()
            #print user_id
            if user_id is not "":
                # If match already found, no need to compare any more
                if not match_found:
                    # Get the image from doctor server
                    get_request_image(user_id)

                    if compare_images(request_photo, input_photo):

                        #transfer_request_medicine(user_id)
                        #print user_id
                        temp_id = user_id
                        match_found = True

                    else:

                        remain_request.append(user_id)
                else:
                    remain_request.append(user_id)

    # Send Signal to Raspberry
    if match_found:
        #Match Request Found
        transfer_request_medicine(temp_id)
        print "1"
    else:
        print "0"

    update_request(remain_request)


if __name__ == "__main__":
    main()
