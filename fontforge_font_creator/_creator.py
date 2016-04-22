#!/usr/bin/env python3
excluded_ranges = list(range(0x0000, 0x0021)) + list(range(0x007F, 0x00A1))


class Ranger:
    def __init__(self, start, stop, excluded_range=None):
        self.current = start
        self.high = stop
        self.stop = stop
        self.excluded_range = excluded_range

    def __iter__(self):
        return self

    def __next__(self):
        if self.current > self.stop:
            raise StopIteration
        else:
            self.current += 1
            while self.current in self.excluded_range:
                self.current += 1
                self.stop += 1
            return self.current

svgs = [
    'accomodation_camp_site.svg',
    'accomodation_caravan_site.svg',
    'accomodation_guest_house.svg',
    'accomodation_hostel.svg',
    'accomodation_hotel.svg',
    'accomodation_motel.svg',
    'accomodation_shelter.svg',
    'amenity_burial_ground.svg',
    'catering_cafe.svg',
    'catering_fastfood.svg',
    'catering_pub.svg',
    'catering_restaurant.svg',
    'default_OSMaxx_marker.svg',
    'destination_castle.svg',
    'destination_memorial.svg',
    'destination_monument.svg',
    'destination_museum.svg',
    'destination_picnic_site.svg',
    'destination_ruin.svg',
    'destination_view_point.svg',
    'destination_wayside_cross.svg',
    'destination_zoo.svg',
    'education_kindergarten.svg',
    'education_school.svg',
    'education_university.svg',
    '_frame.svg',
    'health_clinic.svg',
    'health_dentist.svg',
    'health_doctor.svg',
    'health_hospital.svg',
    'health_pharmacy.svg',
    'leisure_cinema.svg',
    'leisure_golf_course.svg',
    'leisure_stadium.svg',
    'leisure_theatre.svg',
    'military_military_airfield.svg',
    'misc_comm_tower.svg',
    'misc_drinking_water.svg',
    'misc_fountain.svg',
    'misc_hunting_stand.svg',
    'misc_lighthouse.svg',
    'misc_tower.svg',
    'misc_watch_tower.svg',
    'misc_water_tower.svg',
    'misc_water_well.svg',
    'misc_windmill.svg',
    'money_atm.svg',
    'money_bank.svg',
    'money_money_exchange.svg',
    'natural_cave_entrance.svg',
    'natural_peak.svg',
    'natural_rock.svg',
    'natural_sink_hole.svg',
    'natural_tree.svg',
    'natural_volcano.svg',
    'public_building_.svg',
    'public_courthouse.svg',
    'public_embassy.svg',
    'public_fire_station.svg',
    'public_government.svg',
    'public_library.svg',
    'public_market_stand.svg',
    'public_police.svg',
    'public_post_office.svg',
    'public_prison.svg',
    'public_toilet.svg',
    'public_town_hall.svg',
    'shop_car.svg',
    'shop_car_rental.svg',
    'shop_car_repair.svg',
    'shop_kiosk.svg',
    'shop_laundry.svg',
    'shop_supermarket.svg',
    'special_bicycle.svg',
    'special_coniferous.svg',
    'special_deciduous.svg',
    'special_industrial.svg',
    'special_landfill.svg',
    'special_military.svg',
    'special_mining.svg',
    'special_rider.svg',
    'tourism_information.svg',
    'traffic_fuel_station.svg',
    'traffic_gate.svg',
    'traffic_level_crossing.svg',
    'traffic_multi_storey_parking.svg',
    'traffic_parking.svg',
    'transport_airfield.svg',
    'transport_airport.svg',
    'transport_bus_station.svg',
    'transport_bus_stop.svg',
    'transport_bus_stop_and_railway_halt_alternative_M4_one.svg',
    'transport_bus_stop_and_railway_halt_alternative_M4_two.svg',
    'transport_ferry_station.svg',
    'transport_helipad.svg',
    'transport_railway_halt.svg',
    'transport_railway_station.svg',
    'transport_taxi_stand.svg',
    'transport_tram_halt.svg',
    'utility_fossil.svg',
    'utility_hydro.svg',
    'utility_nuclear.svg',
    'utility_plant.svg',
    'utility_pole_and_tower.svg',
    'utility_solar.svg',
    'utility_substation.svg',
    'utility_wind.svg',
    'water_dam.svg',
    'water_reservoir_covered.svg',
    'water_spring.svg',
    'water_waterfall.svg',
    'worship_buddhist.svg',
    'worship_christian.svg',
    'worship_hindu.svg',
    'worship_islamic.svg',
    'worship_jewish.svg',
    'worship_place_of_worship_shinto_taoist.svg',
    'worship_sikh.svg',
]

r = Ranger(0, len(svgs), excluded_ranges)

count = 0
for i in r:
    print("    \"{}\":".format(str(hex(i)).replace('0x', '0x00')))
    print("      filename: \"{}\"".format(svgs[count]))
    count += 1
