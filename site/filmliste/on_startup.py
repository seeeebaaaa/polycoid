from .models import WatchProvider
from .watchprovider_fix import WatchProviders
from .tmdb_utils import tmdb_catch

def create_providers_from_list(provider_list:list):
    new_provider_list =[]
    for provider in provider_list:
        # check if already existent in DB
        if not WatchProvider.objects.filter(provider_id=provider["provider_id"]).exists():
            # add to DB
            print(f"Adding Provider <{provider["provider_name"]}>")
            new_provider = WatchProvider(
                provider_id=provider["provider_id"],
                provider_name=provider["provider_name"],
                logo_path=provider["logo_path"],
                display_priority=provider["display_priority"]
            )
            new_provider_list.append(new_provider)
    if new_provider_list:
        print("Create Objects..")
        WatchProvider.objects.bulk_create(new_provider_list)

def create_from_endpoint(endpoint,watch_region):
    providers = tmdb_catch(endpoint,watch_region=watch_region)
    if not providers:
        print(f"Could not get any WatchProviders for {endpoint}.")
    else:
        create_providers_from_list(providers["results"])

def get_watch_providers(watch_region:str="DE"):
    # get providers for movie
    print("getting movie providers..")
    create_from_endpoint(WatchProviders().watch_providers_movie_list,watch_region=watch_region)
    # get providers for tv
    print("getting tv providers..")
    create_from_endpoint(WatchProviders().watch_providers_tv_list,watch_region=watch_region)


if __name__ == "__main__":
    get_watch_providers()