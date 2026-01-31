from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

i = 0
path_list = ["traffic-photos/traffic_2.png","traffic-photos/img22.jpg","traffic-photos/MUMBAI-CROWD.webp","traffic-photos/traffic1.jpg"]
# Route for the main HTML file
@app.route("/")
def main():

    return render_template("index.html")

# Simulating the VehicleInfo module and function
# from traffic_img import VehicleInfo
# class VehicleInfo:
#     @staticmethod
#     def Vehfun():
#         # Simulate vehicle detection (replace with actual YOLO detection logic)
#         return {"10": {"car": 2, "bike": 1}, "15": {"car": 1, "bus": 1}, "20": {"truck": 1}}

# from traffic_2 import VehicleInfo_8
# @app.route("/new-api", methods=["POST"])
# def calulate_vehicle_count():
#     hari = yolo_object_detection()
#     return jsonify(hari)




# Endpoint for vehicle detection (simulated)
# @app.route("/new-api", methods=["POST"])
# def yolo():
#     vehi = VehicleInfo.Vehfun()  # Call YOLO-like vehicle detection
#     print(vehi)
#     return jsonify(vehi)

# Endpoint for calculating the green time
@app.route("/green-time", methods=['POST'])
def greentime():
    data = yolo_object_detection()  # Get the posted data as JSON
    print(f"Received data for green time calculation: {data}")
    result = green_time(data)  # Calculate the green time
    print(f"Calculated green time: {result}")
    # return jsonify({"vehicle-count":data,"number": result})
    return {"number": result,"vehicle-count":data}

# Global dictionary object with crossing time
dictionary = {
    5: {"car": 3, "bike": 2, "bus": 4, "truck": 5},
    10: {"car": 4, "bike": 3, "bus": 6, "truck": 7},
    15: {"car": 6, "bike": 4, "bus": 8, "truck": 10}
}

# Function to calculate the green time for a distance of 10 meters
def calculate_time_5(dict):
    my_list = []
    if "car" in dict:
        final_time_for_car = dictionary[5]["car"] * dict["car"]
        my_list.append(final_time_for_car)

    if "bike" in dict:
        final_time_for_bike = dictionary[5]["bike"] * dict["bike"]
        my_list.append(final_time_for_bike)

    if "truck" in dict:
        final_time_for_truck = dictionary[5]["truck"] * dict["truck"]
        my_list.append(final_time_for_truck)

    if "bus" in dict:
        final_time_for_bus = dictionary[5]["bus"] * dict["bus"]
        my_list.append(final_time_for_bus)

    else :
        my_list.append(0)

    return max(my_list)

# Similarly for 15 and 20 meters
def calculate_time_10(dict):
    my_list = []
    if "car" in dict:
        final_time_for_car = dictionary[10]["car"] * dict["car"]
        my_list.append(final_time_for_car)

    if "bike" in dict:
        final_time_for_bike = dictionary[10]["bike"] * dict["bike"]
        my_list.append(final_time_for_bike)

    if "truck" in dict:
        final_time_for_truck = dictionary[10]["truck"] * dict["truck"]
        my_list.append(final_time_for_truck)

    if "bus" in dict:
        final_time_for_bus = dictionary[10]["bus"] * dict["bus"]
        my_list.append(final_time_for_bus)
    
    else :
        my_list.append(0)

    return max(my_list)

def calculate_time_15(dict):
    my_list = []
    if "car" in dict:
        final_time_for_car = dictionary[15]["car"] * dict["car"]
        my_list.append(final_time_for_car)

    if "bike" in dict:
        final_time_for_bike = dictionary[15]["bike"] * dict["bike"]
        my_list.append(final_time_for_bike)

    if "truck" in dict:
        final_time_for_truck = dictionary[15]["truck"] * dict["truck"]
        my_list.append(final_time_for_truck)

    if "bus" in dict:
        final_time_for_bus = dictionary[15]["bus"] * dict["bus"]
        my_list.append(final_time_for_bus)
    else :
        my_list.append(0)

    return max(my_list)

# Function to calculate the green time based on the vehicle data at different distances
def green_time(dict):
    green_time_5 = calculate_time_5(dict.get(5, {}))
    green_time_10 = calculate_time_10(dict.get(10, {}))
    green_time_15 = calculate_time_15(dict.get(15, {}))

    final_green_time = green_time_5 + green_time_10 + green_time_15
    if (final_green_time > 60 ):
        final_green_time = 60

    return final_green_time

# from try_traffic_simu import ObjectDetect
import try_traffic_simu
def yolo_object_detection():
    # result = subprocess.run(["python3","try_traffic_simu.py"])
    # instance = ObjectDetect()
    # result = ObjectDetect.yoloo()
    # try:
    #     global i 
    #     print ("value of i",i)
    #     result = try_traffic_simu.yoloo(path_list[i])
    #     i = i + 1
    #     print("output from yolo file : ",result)
    #     return result
    # except IndexError:
    #     i=0
    #     result = try_traffic_simu.yoloo(path_list[i])
    #     i = i + 1
    #     print("output from yolo file : ",result)
    while True:
        global i
        if(i >3):
            i=0
        
        while i <= 3:
            
            print ("value of i :",i)
            result = try_traffic_simu.yoloo(path_list[i])
            print("output from yolo file : ",result)
            i = i+1
            return result
        
            

if __name__ == "__main__":
    app.run(debug=True)

