from math import floor, ceil


# Helper function to convert list values to json

def list_to_json(date_values,sales_data,future_df,score):
  x_values= {}
  y_values= {}

  data_points_iterator =0
  for data_point in date_values:
    x_values[f'{data_points_iterator}'] = str(data_point)
    data_points_iterator+=1

  data_points_iterator=0
  for data_point in sales_data:
    y_values[f'{data_points_iterator}'] = str(floor(data_point))
    data_points_iterator+=1

      
  predicted_results = {
      'x' : x_values,
      'y' : y_values,
      'predict' : str(floor(future_df['forecast'][-1])),
      'rmse' : str(ceil(score)),
      'status': "success"
  }
  return predicted_results 
