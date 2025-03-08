import store_loc
from store_loc import stores_near_me

found_stores=stores_near_me().copy()

#print(found_stores)

max_stores=5
count=0
for store in found_stores:
    store_data=found_stores.get(store)
    print(f"{store}, {store_data[0]}, la {store_data[1]:.2f} km departare.\nLink : https://www.google.com/maps?q={store_data[2]},{store_data[3]}\n")
    count=count+1
    if(count>max_stores):
        break