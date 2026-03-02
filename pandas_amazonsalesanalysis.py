import os
import pandas as pd
import matplotlib.pyplot as plt

sales_data=pd.read_csv('D:\\Kaggle_datasets\\amazon_sales_dataset.csv')
# print(sales_data.dtypes)
# print(sales_data.isnull().sum())
# print(sales_data['order_date'].dtypes,sales_data['ship_date'].dtypes)
sales_data['order_date'] = pd.to_datetime(sales_data['order_date'], errors='coerce')
# print(sales_data['order_date'].dtypes)
sales_data['ship_date']=pd.to_datetime(sales_data['ship_date'],errors='coerce')
# print(sales_data['ship_date'].dtypes)
# print(sales_data.columns.to_list())
# print(sales_data['order_id'].nunique(),sales_data['total_sales'].sum())
# print(f'Unique categories : {sales_data['category'].unique()}')
# print(f'Unique sub-categories : {sales_data['sub_category'].unique()}')
top10_product_bysales=sales_data.groupby('product_name')['total_sales'].sum().sort_values(ascending=False)
# print(top10_product_bysales.head(10))
min_salesamt=sales_data['total_sales'].min()
# print(min_salesamt)
sales_grtthan5k=sales_data[sales_data['total_sales']>5000]
# print(sales_grtthan5k)
sales_disgrt=sales_data[sales_data['discount']>0.0]
# print(sales_disgrt)
# print(sales_data['order_id'].nunique)
total_sales_bycategory=sales_data.groupby('category')['total_sales'].sum()
avgdiscount_bycategory=sales_data.groupby('category')['discount'].mean()
# print(avgdiscount_bycategory)
city_totalsales=sales_data.groupby('city')['total_sales'].sum().sort_values(ascending=False).head(5)
# print(city_totalsales)
sales_data['profit']=sales_data['unit_price']*sales_data['quantity']*(1-sales_data['discount'])
# print(sales_data[['profit','total_sales']])
sales_category_volume=sales_data.groupby('sub_category')['quantity'].sum().sort_values(ascending=False)
# print(sales_category_volume)
avg_order_value=sales_data['total_sales'].mean()
# print(avg_order_value)
product_freq=sales_data['product_id'].value_counts()
most_sold_product=sales_data[sales_data['product_id'].map(product_freq)>20]
# print(most_sold_product)
sales_data_category=sales_data.groupby('category')
for group,groupdf in sales_data_category:
    print(f"Category is :{group}")
    contribution=(groupdf['total_sales'].sum()/sales_data['total_sales'].sum())*100
    # print(groupdf[['product_id','quantity']])
    # print(f"Contributes {contribution}")
sales_data_sorted=sales_data.sort_values(by=['discount','total_sales'],ascending=[False,True])
# print(sales_data_sorted.head(3)[['category','product_id','discount','total_sales']])
# sales_data_sortedbysales=sales_data.groupby('category')['total_sales'].sum().sort_values(ascending=False)
# print(sales_data_sortedbysales)
sales_data['Categorywise_Rank']=sales_data.groupby('category')['total_sales'].rank(ascending=False,method='min')
top_idx=sales_data.groupby('category')['total_sales'].idxmax()
# print(top_idx)
top_products = sales_data.loc[top_idx].reset_index(drop=True)

print(top_products[['category','product_name','sub_category']])
least_sold=sales_data.groupby('category').apply(lambda x:x.nsmallest(2,'total_sales'))
print(least_sold[['product_name','sub_category']].reset_index(drop=True))
print(sales_data.columns.to_list())
sales_data['order_year']=sales_data['order_date'].dt.month
sales_byyear=sales_data.groupby('order_year',as_index=False)['total_sales'].sum()
print(type(sales_byyear))
# print(sales_byyear,sales_data)
sales_data['%month']=sales_byyear['total_sales'].pct_change()* 100
print(sales_data['%month'])
sales_bycity=sales_data.groupby('city',as_index=False)['total_sales'].sum()
total_revenue=sales_bycity['total_sales'].sum()
sales_bycity['revenue%']=(sales_bycity['total_sales']/total_revenue*100).round(2)
print(sales_bycity)
# print(sales_data['product_id'].value_counts)
avg_quantity_city=sales_data.groupby('city',as_index=False)['quantity'].mean()
print(avg_quantity_city)
highest_quantity=avg_quantity_city.loc[avg_quantity_city['quantity'].idxmax()]
print(highest_quantity)
# for grp,grpdf in sales_data.groupby('city'):
    # topproducts=grpdf.sort_values('total_sales').head(3)
    # print(f"Top products in city {grp} are {topproducts['product_id']}")
sales_byregionprod=sales_data.groupby(['city','product_id'],as_index=False)['total_sales'].sum()
sales_data['Prod_rank']=sales_byregionprod.groupby('city')['total_sales'].rank(method='first',ascending=False)
print(sales_data[sales_data['Prod_rank']<=3])
sales_data_sortedbydate=sales_data.sort_values('order_date',ascending=True)
sales_data_sortedbydate['Cumulative_sales']=sales_data_sortedbydate['total_sales'].cumsum()
print(sales_data_sortedbydate['Cumulative_sales'])
sales_productfreq=sales_data.groupby(['product_id','customer_id'],as_index=False).agg(product_freq=('order_id','count'))
print(sales_productfreq)
repeatedcustomer=sales_productfreq[sales_productfreq['product_freq']>1]
print(repeatedcustomer)
#Sales comparison with and without discount
sales_data['Pricewithoutdiscount']=sales_data['unit_price']*sales_data['quantity']
sales_data['Pricewithdiscount']=sales_data['Pricewithoutdiscount']*(1-sales_data['discount'])
totalsalewithdiscount=sales_data['Pricewithdiscount'].sum()
totalsalewithoutdiscount=sales_data['Pricewithoutdiscount'].sum()
salediff=totalsalewithoutdiscount-totalsalewithdiscount
salediffper=(salediff/totalsalewithoutdiscount*100).round(2)
# print(f"Sale comparison with and without discount {salediff} {salediffper}")
#High discounted product
sales_highdiscounted=sales_data.sort_values(by=['discount','quantity'],ascending=[False,True])
# print(f"High discounted products {sales_highdiscounted[['total_sales','discount','quantity']]}")
sales_data['salesdiscount']=sales_data['unit_price']*sales_data['quantity']*sales_data['discount']
product_discount=sales_data.groupby('product_id',as_index=False).agg(discountper=('discount','mean'),totaldiscountper=('salesdiscount','sum'))
# print(f"review: {product_discount}")
sort_by_discountper=product_discount.sort_values(by='discountper',ascending=False)
sort_by_discountamt=product_discount.sort_values(by='totaldiscountper',ascending=False)
# print(f"sorted {sort_by_discountper} ,{sort_by_discountamt}")
#ABC analysis on sales
sales_analysis=sales_data.groupby('product_id').agg(salestotal=('total_sales','sum'))
sales_analysis['Rank_sales']=sales_analysis['salestotal'].rank(ascending=False)
# print(f"Sales analysis {sales_analysis}")
sales_analysis['cum_sales']=sales_analysis['salestotal'].cumsum()
sales_analysis['cum_pct']=(sales_analysis['cum_sales']/sales_analysis['salestotal'].sum()*100).round(2)
def revenue_catgory(pct):
    if pct >= 70:
        return 'A'
    elif pct >= 20:
        return 'B'
    else:
        return 'C'
sales_analysis['revenue_category']=sales_analysis['cum_pct'].apply(revenue_catgory)
# print(sales_analysis)
#Find outliers in dataset
Q1=sales_data['total_sales'].quantile(0.25)
Q3=sales_data['total_sales'].quantile(0.75)
IQR=Q3-Q1
lower_bound=Q1-(1.5*IQR)
upper_bound=Q3+(1.5*IQR)
sales_data_outliers=sales_data[(sales_data['total_sales'] < lower_bound) | (sales_data['total_sales'] > upper_bound)]
print(f"lower_bound {lower_bound} , upper_bound {upper_bound} Outliers are {sales_data_outliers['total_sales']}")
#Seasonal analysis on month basis
sales_data['order_month']=sales_data['order_date'].dt.month
sales_data_monthwise=sales_data.groupby('order_month')['total_sales'].sum()
print(f"Monthwise summary of sales {sales_data_monthwise}")
#Product dependent on discount
sales_data['discount_dependent_val']=sales_data['Pricewithdiscount']/sales_data['Pricewithoutdiscount']
sales_highlydiscount_oriented=sales_data[sales_data['discount_dependent_val']>2]
print(f"Sales that are highly dependent on discount {sales_data['discount_dependent_val']}")
plt.plot(sales_data['order_month'].astype(str), sales_data['total_sales'], marker='o')
plt.title("Monthly Aggregated Sales")
plt.xlabel("Month")
plt.ylabel("Total Sales")
plt.xticks(rotation=45)
plt.show()
