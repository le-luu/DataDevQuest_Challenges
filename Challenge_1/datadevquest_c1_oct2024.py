import tableauserverclient as TSC

# Set the credentials to connect to Tableau cloud with TSC
server_url = "https://10ax.online.tableau.com"  
site_name = "your_site_name" 
token_name = "your_token_name" 
personal_access_token = "your_personal_access_token" 

def find_view_by_name(server_url,site_name,token_name, personal_access_token,search_view):
    
    #Initialize the empty list for view_list to store the list of dictionaries later
    view_list = []

    # From the credentials input, create a connection with TSC
    tableau_auth = TSC.PersonalAccessTokenAuth(token_name, personal_access_token, site_id=site_name)
    server = TSC.Server(server_url, use_server_version=True)

    try:
        # Authenticate the credentials and connect
        with server.auth.sign_in(tableau_auth):
            all_views, pagination_item = server.views.get()

            # Iterate to each view in all_views, if found view name matches the search view (case-insensitive), 
            # then store each view from all_views into the matched_views list
            matched_views = []
            for view in all_views:
                if search_view.lower() in view.name.lower():
                    matched_views.append(view)
                    
            #If there are values in the matched_views list
            if matched_views:
                print("\nFound the following view(s): ")
                #for each view in the matched_view
                for view in matched_views:
                    
                    #create an empty dictionaty to store the data with the key and value 
                    #in View Name/ID, Workbook name, Project Name, View URL
                    view_dict = {}

                    # Store the view name and id in the list view_name, view_id
                    view_dict["View Name"] = view.name
                    view_dict["View ID"] = view.id
                    
                    # Get the view item and workbook details
                    view_item = server.views.get_by_id(view.id)
                    workbook_item = server.workbooks.get_by_id(view_item.workbook_id)

                    # Store workbook name and project name
                    view_dict["Workbook Name"] = workbook_item.name
                    view_dict["Project Name"] = workbook_item.project_name

                    # concatnate server url, sitename, workbook name,view name to create a full path
                    # trim the space in workbook_item and view_name
                    view_url_item = f"{server_url}/#/site/{site_name}/views/{workbook_item.name.replace(' ','')}/{view.name.replace(' ','')}"
                    view_dict["View URL"] = view_url_item
                    
                    #append the view dictionary into the view list 
                    view_list.append(view_dict)
            
            #sign out the server after iterating all values in matched_views
            server.auth.sign_out()
    #catch the error if something is wrong during the authentication step 
    except:
        print("Something is wrong")
        
    #return the list of view including dictionary
    return view_list


def main():
    
    # User enter the view want to search for
    search_view = input("Enter the name of the Tableau view you want to search for: ")
    print("\nSearching for views ...")
    
    #call the function find_view_by_name and passing the credentials info into this function
    view_data = find_view_by_name(server_url,site_name,token_name, personal_access_token,search_view)
    
    #if found the result in view_data
    if view_data:
        #then, iterate to each view in the view_data
        for i,view in enumerate(view_data,start=1):
            #for each result, print out the view name, view id, workbook name, project name and view url
            print(f"\n{i})")
            for key,value in view.items():
                print(f"- {key}: {value}")
        print()
    #if cannot find the view in Cloud
    else:
        print("\nUnfortunately, we cannot found the view you want")
    #the finding view name process end
    print("\nProcess completed successfully")
        
if __name__ == "__main__":
    main()