'''
Author: Mingyang Li 
Date: 04/12/2020
Description: 
This class focuses on migrating Vend POS supply price to Shopify products in cvs format. 
Still need to manually upload the csv into Shopify, but this code does the majority of the heavy-lifting
'''

class Vend_Shopify_Product_Migration:
    def __init__(self, vend_products_csv_file, shopify_products_csv_file, csv_to_write):
        self.vend_products_csv_file = vend_products_csv_file
        self.shopify_products_csv_file = shopify_products_csv_file
        self.csv_to_write = csv_to_write
        self.vend_sku_and_supply_price = {}
        self.array_shopify_sku = []
        # The shopify_products_file is a csv exported from shopify store admin using an app called excelify 
        # You only need to export Shopify products by: variant SKU and (variant cost or variant barcode) as we are only interested in updating these fields

    def __str__(self):
        return "Migration instantiated."
    
    def get_vend_products_csv_file(self):
        return self.vend_products_csv_file

    def get_shopify_products_csv_file(self):
        return self.shopify_products_csv_file
    
    def get_csv_to_write(self):
        return self.csv_to_write

    def get_dict_vend_supply_price_by_sku(self):
        import csv
        vend_file = self.vend_products_csv_file
        with open(vend_file, encoding='utf-8', mode='r') as csv_file:
            vend_csv_header = csv.reader(csv_file)
            for line in vend_csv_header:
                vend_sku = line[2]
                vend_supply_price = line[16] 
                self.vend_sku_and_supply_price[vend_sku] = vend_supply_price
        return self.vend_sku_and_supply_price
    
    def print_vend_supply_price_by_sku(self):
        for e in sorted(self.vend_sku_and_supply_price.keys()):
            print(e, self.vend_sku_and_supply_price[e])

    def get_array_of_shopify_sku(self):
        shopify_file = self.get_shopify_products_csv_file()
        import csv
        with open(shopify_file) as csv_file:
            shopify_csv_header = csv.reader(csv_file)
            for row in shopify_csv_header:
                self.array_shopify_sku.append(row[0])
            return self.array_shopify_sku
    
    def print_array_shopify_sku(self):
        for e in self.array_shopify_sku:
            print(e)

    def print_vend_products_with_zero_supply_price(self, vend_csv_to_read):
        print('Start scanning for vend products that do not have a supply price \n')
        for line in vend_csv_to_read:
            supply_price = line[16]
            if supply_price == '0':
                print('sku:', line[2])
                print('supply_price:', supply_price, '\n')
        print('Scanning done!')

    # writes sku and cost on an empty csv file in shopify's import format
    def update_shopify_item_cost(self):
        import csv
        file = self.get_csv_to_write()
        ct = 1
        with open(file, mode='w') as csv_file:
            header = ['Variant SKU', 'Variant Cost']
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(header)
            for key in self.vend_sku_and_supply_price.keys():
                if ct == 1:
                    ct += 1
                else:
                    sku = key
                    if sku in self.array_shopify_sku:
                        cost = self.vend_sku_and_supply_price[sku]
                        csv_writer.writerow([sku] + [cost])
                        print('wrote on csv ' + str(ct) + ' times')
                        ct += 1

    def get_out_of_stock_vend_products(self):
        pass
  
vend_file = 'vend-products-active-test.csv'
shopify_file = 'shopify-test-sku-n-cost.csv'
file_to_write = 'file_to_write.csv'
migration = Vend_Shopify_Product_Migration(vend_file, shopify_file, file_to_write)

dict_vend_supply_price_by_sku = migration.get_dict_vend_supply_price_by_sku()
array_shopify_sku_and_cost = migration.get_array_of_shopify_sku()

migration.update_shopify_item_cost()