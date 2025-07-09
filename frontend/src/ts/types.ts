export interface Product {
  id: string
  name: string
  price: number
}

export interface Order {
  id: string
  name: string
  description: string
  total_amount: number
  created_at: string
  updated_at: string
  products: string[]
  product_details?: Product[]
}
