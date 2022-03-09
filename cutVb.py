if __name__ == '__main__':
    text = 'https://www.booking.com/hotel/vn/green-meadow-villa-amp-cafe.vi.html?label=888&sid=048a9fe95aafeade797e607e6d5e4b2b&aid=1541467&ucfs=1&arphpl=1&checkin=2022-02-15&checkout=2022-02-16&dest_id=-3712045&dest_type=city&group_adults=2&req_adults=2&no_rooms=1&group_children=0&req_children=0&hpos=1&hapos=1&sr_order=popularity&srpvid=041934fe52ea00d4&srepoch=1644823934&all_sr_blocks=459455002_344799751_0_0_0&highlighted_blocks=459455002_344799751_0_0_0&matching_block_id=459455002_344799751_0_0_0&sr_pri_blocks=459455002_344799751_0_0_0__45124000&from=searchresults#hotelTmpl'
    rs = text.index('?');
    new_text = text[0:rs]
    print(new_text)