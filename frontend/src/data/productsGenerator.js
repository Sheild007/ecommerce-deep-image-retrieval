// Product data from CSV files with real image URLs and PKR pricing

const imageMap = {
  '15970': 'http://assets.myntassets.com/v1/images/style/properties/7a5b82d1372a7a5c6de67ae7a314fd91_images.jpg',
  '39386': 'http://assets.myntassets.com/v1/images/style/properties/4850873d0c417e6480a26059f83aac29_images.jpg',
  '59263': 'http://assets.myntassets.com/v1/images/style/properties/Titan-Women-Silver-Watch_b4ef04538840c0020e4829ecc042ead1_images.jpg',
  '21379': 'http://assets.myntassets.com/v1/images/style/properties/8153dc35d9a5420eeb93922067137db6_images.jpg',
  '53759': 'http://assets.myntassets.com/v1/images/style/properties/Puma-Men-Grey-T-shirt_32668f8a61454d0cc028a808cf21b383_images.jpg',
  '1855': 'http://assets.myntassets.com/v1/images/style/properties/9c1b19682ecf926c296f520d5d6e0972_images.jpg',
  '30805': 'http://assets.myntassets.com/v1/images/style/properties/06e9d4231254fdb2c7fe967ad413ad7b_images.jpg',
  '26960': 'http://assets.myntassets.com/v1/images/style/properties/45ddbc6a15140556214e15923244755b_images.jpg',
  '29114': 'http://assets.myntassets.com/v1/images/style/properties/4ca8848ab441378a392d9d5bf0b0f3c7_images.jpg',
  '30039': 'http://assets.myntassets.com/v1/images/style/properties/Skagen-Men-Black-Watch_4982b2b1a76a85a85c9adc8b4b2d523a_images.jpg',
  '9204': 'http://assets.myntassets.com/v1/images/style/properties/051d64772f1b38ff476fbf0a807f365a_images.jpg',
  '48123': 'http://assets.myntassets.com/v1/images/style/properties/8eee4563e14cf451b07f27761fd6535f_images.jpg',
  '18653': 'http://assets.myntassets.com/v1/images/style/properties/53690e3f396f411e184b249672d6ebae_images.jpg',
  '47957': 'http://assets.myntassets.com/v1/images/style/properties/Murcia-Women-Blue-Handbag_13cfaff26872c298112a8e7da15c1e1d_images.jpg',
  '46885': 'http://assets.myntassets.com/v1/images/style/properties/5cab6a2305d0e63142f721228aa6d293_images.jpg',
  '12369': 'http://assets.myntassets.com/v1/images/style/properties/8bc9be576081baae77e8561b1132288f_images.jpg',
  '29928': 'http://assets.myntassets.com/v1/images/style/properties/Police-Men-Black-Dial-Watch_5bd8cae4fc61052a6f00cfcd69c4a936_images.jpg',
  '42419': 'http://assets.myntassets.com/v1/images/style/properties/f3964f76c78edd85f4512d98b26d52e9_images.jpg',
  '51832': 'http://assets.myntassets.com/v1/image/style/properties/51832/Bwitch-Beige-Full-Coverage-Bra-BW335_1_d516fa94f14f0a5ecc90df7754390eb5.jpg',
  '47359': 'http://assets.myntassets.com/v1/images/style/properties/b14c7bf275c6edca3e849200fb7cbf6c_images.jpg',
}

const baseProducts = [
  { id: '15970', name: 'Turtle Check Men Shirt', gender: 'Men', masterCategory: 'Apparel', subCategory: 'Topwear', articleType: 'Shirts', color: 'Navy Blue', season: 'Fall', year: 2011, usage: 'Casual', basePriceINR: 1299 },
  { id: '39386', name: 'Peter England Men Jeans', gender: 'Men', masterCategory: 'Apparel', subCategory: 'Bottomwear', articleType: 'Jeans', color: 'Blue', season: 'Summer', year: 2012, usage: 'Casual', basePriceINR: 2499 },
  { id: '59263', name: 'Titan Women Watch', gender: 'Women', masterCategory: 'Accessories', subCategory: 'Watches', articleType: 'Watches', color: 'Silver', season: 'Winter', year: 2016, usage: 'Casual', basePriceINR: 3999 },
  { id: '21379', name: 'Manchester United Track Pants', gender: 'Men', masterCategory: 'Apparel', subCategory: 'Bottomwear', articleType: 'Track Pants', color: 'Black', season: 'Fall', year: 2011, usage: 'Casual', basePriceINR: 1899 },
  { id: '53759', name: 'Puma Men T-shirt', gender: 'Men', masterCategory: 'Apparel', subCategory: 'Topwear', articleType: 'Tshirts', color: 'Grey', season: 'Summer', year: 2012, usage: 'Casual', basePriceINR: 899 },
  { id: '1855', name: 'Inkfruit Men T-shirt', gender: 'Men', masterCategory: 'Apparel', subCategory: 'Topwear', articleType: 'Tshirts', color: 'Grey', season: 'Summer', year: 2011, usage: 'Casual', basePriceINR: 799 },
  { id: '30805', name: 'Fabindia Men Shirt', gender: 'Men', masterCategory: 'Apparel', subCategory: 'Topwear', articleType: 'Shirts', color: 'Green', season: 'Summer', year: 2012, usage: 'Ethnic', basePriceINR: 1499 },
  { id: '26960', name: 'Jealous 21 Women Shirt', gender: 'Women', masterCategory: 'Apparel', subCategory: 'Topwear', articleType: 'Shirts', color: 'Purple', season: 'Summer', year: 2012, usage: 'Casual', basePriceINR: 1599 },
  { id: '29114', name: 'Puma Men Socks', gender: 'Men', masterCategory: 'Accessories', subCategory: 'Socks', articleType: 'Socks', color: 'Navy Blue', season: 'Summer', year: 2012, usage: 'Casual', basePriceINR: 499 },
  { id: '30039', name: 'Skagen Men Watch', gender: 'Men', masterCategory: 'Accessories', subCategory: 'Watches', articleType: 'Watches', color: 'Black', season: 'Winter', year: 2016, usage: 'Casual', basePriceINR: 4999 },
  { id: '9204', name: 'Puma Men Shoes', gender: 'Men', masterCategory: 'Footwear', subCategory: 'Shoes', articleType: 'Casual Shoes', color: 'Black', season: 'Summer', year: 2011, usage: 'Casual', basePriceINR: 4499 },
  { id: '48123', name: 'Fossil Women Belt', gender: 'Women', masterCategory: 'Accessories', subCategory: 'Belts', articleType: 'Belts', color: 'Black', season: 'Summer', year: 2012, usage: 'Casual', basePriceINR: 1899 },
  { id: '18653', name: 'Fila Men Slippers', gender: 'Men', masterCategory: 'Footwear', subCategory: 'Flip Flops', articleType: 'Flip Flops', color: 'Black', season: 'Fall', year: 2011, usage: 'Casual', basePriceINR: 1299 },
  { id: '47957', name: 'Murcia Women Handbag', gender: 'Women', masterCategory: 'Accessories', subCategory: 'Bags', articleType: 'Handbags', color: 'Blue', season: 'Summer', year: 2012, usage: 'Casual', basePriceINR: 2999 },
  { id: '46885', name: 'Ben 10 Boys Slippers', gender: 'Boys', masterCategory: 'Footwear', subCategory: 'Flip Flops', articleType: 'Flip Flops', color: 'Navy Blue', season: 'Fall', year: 2012, usage: 'Casual', basePriceINR: 1099 },
  { id: '12369', name: 'Reid & Taylor Men Shirt', gender: 'Men', masterCategory: 'Apparel', subCategory: 'Topwear', articleType: 'Shirts', color: 'Purple', season: 'Fall', year: 2011, usage: 'Formal', basePriceINR: 3299 },
  { id: '29928', name: 'Police Men Watch', gender: 'Men', masterCategory: 'Accessories', subCategory: 'Watches', articleType: 'Watches', color: 'Black', season: 'Winter', year: 2016, usage: 'Casual', basePriceINR: 5999 },
  { id: '42419', name: 'Gini & Jony Girls Top', gender: 'Girls', masterCategory: 'Apparel', subCategory: 'Topwear', articleType: 'Tops', color: 'White', season: 'Summer', year: 2012, usage: 'Casual', basePriceINR: 799 },
  { id: '51832', name: 'Bwitch Women Bra', gender: 'Women', masterCategory: 'Apparel', subCategory: 'Innerwear', articleType: 'Bra', color: 'Beige', season: 'Summer', year: 2016, usage: 'Casual', basePriceINR: 1599 },
  { id: '47359', name: 'Baggit Women Handbag', gender: 'Women', masterCategory: 'Accessories', subCategory: 'Bags', articleType: 'Handbags', color: 'Brown', season: 'Summer', year: 2012, usage: 'Casual', basePriceINR: 3499 },
]

const generateProducts = () => {
  const products = []
  let productId = 1000

  // Generate 20,000 products by variations of base products
  for (let i = 0; i < 20000; i++) {
    const baseProduct = baseProducts[i % baseProducts.length]
    
    // Add price variation
    const priceVariation = 0.8 + Math.random() * 0.4 // ±20% price variation
    const pricePKR = Math.round((baseProduct.basePriceINR * 1.8) * priceVariation / 50) * 50 // Convert INR to PKR (1.8x), round to 50
    
    const imageUrl = imageMap[baseProduct.id] || 'https://via.placeholder.com/300x300/cccccc/ffffff?text=No+Image'
    
    products.push({
      id: productId++,
      name: baseProduct.name,
      gender: baseProduct.gender,
      masterCategory: baseProduct.masterCategory,
      subCategory: baseProduct.subCategory,
      articleType: baseProduct.articleType,
      color: baseProduct.color,
      season: baseProduct.season,
      year: baseProduct.year,
      usage: baseProduct.usage,
      price: pricePKR,  // Price in PKR (Pakistani Rupees)
      image: imageUrl,  // Real image URL from images.csv
      brand: baseProduct.name.split(' ')[0],
    })
  }

  return products
}

export default generateProducts
