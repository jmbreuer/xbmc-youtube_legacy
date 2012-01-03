import BaseTestCase
import nose
import sys


class TestYouTubeShowsScraper(BaseTestCase.BaseTestCase):
    def ttest_plugin_should_scrape_shows_category_listing_correctly(self):
        self.navigation.listMenu({"scraper": "shows", "path": "/root/explore/shows", "folder": "true"})

        self.assert_directory_count_greater_than_or_equals(10)
        self.assert_directory_count_less_than_or_equals(51)
        self.assert_directory_is_a_folder_list()
        self.assert_directory_item_urls_contain("category")
        self.assert_directory_items_should_have_thumbnails()
    
    def ttest_plugin_should_scrape_show_list_correctly(self):
        
        self.navigation.listMenu({"scraper": "shows", "path": "/root/explore/shows", "category": "comedy%3Ffeature%3Dsh_c%26amp%3Bpt%3Dg"})
        
        self.assert_directory_count_greater_than_or_equals(10)
        self.assert_directory_count_less_than_or_equals(51)
        self.assert_directory_is_a_folder_list()
        self.assert_directory_item_urls_contain("show")
        self.assert_directory_items_should_have_external_thumbnails()
    
    def ttest_plugin_should_scrape_show_episode_video_list_correctly(self):
        self.navigation.listMenu({"scraper": "shows", "path": "/root/explore/trailers/current", "show": "blackboxtv?feature=sh_b_dr_4_3"})
        
        self.assert_directory_count_greater_than_or_equals(5)
        self.assert_directory_count_less_than_or_equals(51)
        self.assert_directory_is_a_video_list()
        self.assert_directory_contains_almost_only_unique_video_items()
        self.assert_directory_items_should_have_external_thumbnails()

    def ttest_plugin_should_scrape_show_season_folder_list_correctly(self):
        self.navigation.listMenu({"scraper": "shows", "path": "/root/explore/trailers/current", "show": "minecraft?feature=sh_gm_show_1_1"})
        
        self.assert_directory_count_greater_than_or_equals(5)
        self.assert_directory_count_less_than_or_equals(51)
        self.assert_directory_is_a_folder_list()
        self.assert_directory_item_urls_contain("season")

    def ttest_plugin_should_scrape_show_season_episode_video_list_correctly(self):
        sys.modules["__main__"].settings.setSetting("perpage", "6")
        self.navigation.listMenu({"scraper": "shows", "path": "/root/explore/trailers/current", "show": "minecraft?feature=sh_gm_show_1_1", "season": "Mods"})
        
        self.assert_directory_count_greater_than_or_equals(30)
        self.assert_directory_count_less_than_or_equals(51)
        self.assert_directory_is_a_video_list()
        self.assert_directory_contains_almost_only_unique_video_items()
        self.assert_directory_items_should_have_external_thumbnails()

    def ttest_plugin_should_scrape_show_season_episode_video_list_page_2_correctly(self): # Epic failure
        self.navigation.listMenu({"scraper": "shows", "path": "/root/explore/trailers/current", "show": "minecraft?feature=sh_gm_show_1_1", "season": "SoI", "page": "1"})
        
        self.assert_directory_count_greater_than_or_equals(10)
        self.assert_directory_count_less_than_or_equals(51)
        self.assert_directory_is_a_video_list()
        self.assert_directory_contains_almost_only_unique_video_items()
        self.assert_directory_items_should_have_thumbnails()

if __name__ == "__main__":
    nose.runmodule()
