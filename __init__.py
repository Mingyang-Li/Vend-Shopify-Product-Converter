'''
Author: Mingyang Li 
Date: 03/12/2020
Description: This class main focuses on migrating Vend POS product barcode and supply price to Shopify products in cvs format. 
You still need to manually upload the updated csv into Shopify to complete the migration, but this code does the majority of the heavy-lifting
'''

class Vend_Shopify_Product_Migration:
    def __init__(self, vend_products_file, shopify_products_file):
        self.vend_products_file = vend_products_file
        self.shopify_products_file = shopify_products_file
        self.vend_sku_and_barcode = {}
        self.vend_sku_and_supply_price = {}
        # The shopify_products_file is a csv exported from shopify store admin using an app called excelify 
        # You only need to export Shopify products by: variant SKU and (variant cost or variant barcode) as we are only interested in updating these fields

    def __str__(self):
        return "Migration instantiated."
    
    def get_vend_products_file(self):
        return self.vend_products_file

    def get_shopify_products_file(self):
        return self.shopify_products_file
        
    # this method opens the csv only
    def open_csv(self, file):
        import csv
        file_content = []
        with open(file, encoding='utf-8', mode='r') as csv_file:
            csv_reader = csv.reader(csv_file)
            for line in csv_reader:
                file_content.append(line)
        return file_content

    def get_vend_sku_and_barcode(self, csv_content_array):
        for line in csv_content_array:
            vend_sku = line[2]
            # placeholder index for barcode as unknown
            vend_barcode = line[0] 
            self.vend_sku_and_barcode[vend_sku] = vend_barcode
        return self.vend_sku_and_barcode

    def get_vend_supply_price_by_sku(self, csv_content_array):
        for line in csv_content_array:
            vend_sku = line[2]
            vend_supply_price = int(line[16])
            self.vend_sku_and_supply_price[vend_sku] = vend_supply_price
        return self.vend_sku_and_supply_price

    def get_vend_products_with_zero_supply_price(self, csv_content_array):
        print('Start scanning for active vend products that do not have a supply price \n')
        for line in csv_content_array:
            supply_price = line[16]
            if supply_price == '0':
                print('sku:', line[2])
                print('supply_price:', supply_price, '\n')
        print('Scanning done!')

    def update_shopify_item_cost(self, shopify_products_csv, vend_sku_and_supply_price):
        for pair in vend_sku_and_supply_price:
            vend_sku = pair[0]
            vend_supply_price = pair[1]
            for row in shopify_products_csv:
                shopify_sku = row[0]
                if vend_sku == shopify_sku:
                    row[1] = vend_supply_price
                
    def update_shopify_barcode(self, shopify_products_csv, vend_sku_and_barcode):
        pass

vend_file = 'vend-products-active.csv'
shopify_file = 'shopify-products-test.csv'
migration = Vend_Shopify_Product_Migration(vend_file, shopify_file)

vend_csv = migration.open_csv(vend_file)
vend_sku_and_barcode = migration.get_vend_sku_and_barcode(vend_csv)
shopify_csv = migration.open_csv(shopify_file)
for e in vend_csv:
    print(e)
