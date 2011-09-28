# -*- coding: utf-8 -*-
import nose
import BaseTestCase
from mock import Mock
import sys
from  YouTubePlaylistControl import YouTubePlaylistControl 

class TestYouTubePlaylistControl(BaseTestCase.BaseTestCase):
	
	def test_playAll_should_call_getPlayList_if_playlist_entry_in_params(self):
		control = YouTubePlaylistControl()
		control.getPlayList = Mock()
		control.getPlayList.return_value = ""
		
		control.playAll({"playlist":"someid"})
		
		control.getPlayList.assert_called_with({"playlist":"someid", 'fetch_all': 'true'})
		
	def test_playAll_should_call_getDiscoSearch_if_scraper_is_disco_search_in_params(self):
		control = YouTubePlaylistControl()
		control.getDiscoSearch = Mock()
		control.getDiscoSearch.return_value = ""
		
		control.playAll({"search_disco":"some_search"})
		
		control.getDiscoSearch.assert_called_with({"search":"some_search","search_disco":"some_search", 'fetch_all': 'true'})
				
	def test_playAll_should_call_getFavorites_if_user_feed_is_favorites_in_params(self):
		control = YouTubePlaylistControl()
		control.getFavorites = Mock()
		control.getFavorites.return_value = ""
		
		control.playAll({"user_feed":"favorites"})
		
		control.getFavorites.assert_called_with({"user_feed":"favorites", 'fetch_all': 'true'})
		
	def test_playAll_should_call_getWatchLater_if_scraper_is_watch_later_in_params(self):
		control = YouTubePlaylistControl()
		control.getWatchLater = Mock()
		control.getWatchLater.return_value = ""
		
		control.playAll({"scraper":"watch_later"})
		
		control.getWatchLater.assert_called_with({"scraper":"watch_later", 'fetch_all': 'true'})
		
	def test_playAll_should_call_getLikedVideos_if_scraper_is_liked_videos_in_params(self):
		control = YouTubePlaylistControl()
		control.getLikedVideos = Mock()
		control.getLikedVideos.return_value = ""
		
		control.playAll({"scraper":"liked_videos"})
		
		control.getLikedVideos.assert_called_with({"scraper":"liked_videos", 'fetch_all': 'true'})
		
	def test_playAll_should_call_getArtist_if_scraper_is_music_artist_in_params(self):		
		control = YouTubePlaylistControl()
		control.getArtist = Mock()
		control.getArtist.return_value = ""
		
		control.playAll({"scraper":"music_artists"})
		
		control.getArtist.assert_called_with({"scraper":"music_artists", 'fetch_all': 'true'})
		
	def test_playAll_should_call_getRecommended_if_scraper_is_recommended_in_params(self):
		control = YouTubePlaylistControl()
		control.getRecommended = Mock()
		control.getRecommended.return_value = ""
		
		control.playAll({"scraper":"recommended"})
		
		control.getRecommended.assert_called_with({"scraper":"recommended", 'fetch_all': 'true'})
		
	def test_playAll_should_call_getNewSubscriptions_if_user_feed_is_subscriptions_in_params(self):
		control = YouTubePlaylistControl()
		control.getNewSubscriptions = Mock()
		control.getNewSubscriptions.return_value = ""
		
		control.playAll({"user_feed":"newsubscriptions"})
		
		control.getNewSubscriptions.assert_called_with({"user_feed":"newsubscriptions", 'fetch_all': 'true'})
		
	def test_playAll_should_not_call_xbmc_player_if_params_is_empty(self):
		control = YouTubePlaylistControl()
		
		control.playAll({})
		
		assert(sys.modules["__main__"].xbmc.Player.call_count == 0)
		assert(sys.modules["__main__"].xbmc.Player().call_count == 0)
		
	def test_playAll_should_call_xbmc_player_stop_if_player_is_playing(self):
		control = YouTubePlaylistControl()
		control.getPlayList = Mock()
		control.getPlayList.return_value = [{"Title":"someTitle", "videoid":"some_id","thumbnail":"some_thumbnail"}]
		
		control.playAll({"playlist":"someid"})
		
		sys.modules["__main__"].xbmc.Player.assert_called_with()
		sys.modules["__main__"].xbmc.Player().isPlaying.assert_called_with()
		sys.modules["__main__"].xbmc.Player().stop.assert_called_with()
		
	def test_playAll_should_call_xbmc_PlayList_clear_if_results_is_not_empty(self):
		playlist_value = Mock()
		sys.modules["__main__"].xbmc.PlayList.return_value = playlist_value
		control = YouTubePlaylistControl()
		control.getPlayList = Mock()
		control.getPlayList.return_value = [{"Title":"someTitle", "videoid":"some_id","thumbnail":"some_thumbnail"}]
		
		control.playAll({"playlist":"someid"})
		
		playlist_value.clear.assert_called_with()
		
	def test_playAll_should_call_xbmc_player_shuffle_if_shuffle_is_in_params(self):
		playlist_value = Mock()
		sys.modules["__main__"].xbmc.PlayList.return_value = playlist_value
		control = YouTubePlaylistControl()
		control.getPlayList = Mock()
		control.getPlayList.return_value = [{"Title":"someTitle", "videoid":"some_id","thumbnail":"some_thumbnail"}]
		
		control.playAll({"playlist":"someid","shuffle":"true"})
		
		sys.modules["__main__"].xbmc.Player.assert_called_with()
		sys.modules["__main__"].xbmc.Player().isPlaying.assert_called_with()
		sys.modules["__main__"].xbmc.Player().stop.assert_called_with()
		playlist_value.shuffle.assert_called_with()
		
	def test_playAll_should_correctly_queue_all_items_in_result_list(self):
		playlist_value = Mock()
		sys.modules["__main__"].xbmc.PlayList.return_value = playlist_value
		control = YouTubePlaylistControl()
		control.getPlayList = Mock()
		control.getPlayList.return_value = [{"Title":"someTitle1", "videoid":"some_id1","thumbnail":"some_thumbnail1"},{"Title":"someTitle2", "videoid":"some_id2","thumbnail":"some_thumbnail2"}]
		
		control.playAll({"playlist":"someid","shuffle":"true"})
		
		assert(playlist_value.add.call_count == 2)
	
	def test_playAll_should_start_playback_of_playlist_if_result_list_is_not_empty(self):
		playlist_value = Mock()
		sys.modules["__main__"].xbmc.PlayList.return_value = playlist_value
		control = YouTubePlaylistControl()
		control.getPlayList = Mock()
		control.getPlayList.return_value = [{"Title":"someTitle1", "videoid":"some_id1","thumbnail":"some_thumbnail1"},{"Title":"someTitle2", "videoid":"some_id2","thumbnail":"some_thumbnail2"}]
		
		control.playAll({"playlist":"someid"})
		
		sys.modules["__main__"].xbmc.executebuiltin.assert_called_with('playlist.playoffset(video , 0)')
		
	def test_queueVideo_should_handle_a_list_of_video_ids_seperated_by_a_comma(self):
		playlist_value = Mock()
		sys.modules["__main__"].xbmc.PlayList.return_value = playlist_value
		sys.modules["__main__"].core.getBatchDetails.return_value = ({"apierror":""},303)
		control = YouTubePlaylistControl()
		control.getPlayList = Mock()
		control.getPlayList.return_value = [{"Title":"someTitle1", "videoid":"some_id1","thumbnail":"some_thumbnail1"},{"Title":"someTitle2", "videoid":"some_id2","thumbnail":"some_thumbnail2"}]
		
		control.queueVideo({"videoid":"someid1,someid2,someid3"})
		
		sys.modules["__main__"].core.getBatchDetails.assert_called_with(['someid1', 'someid2', 'someid3'], {'videoid': 'someid1,someid2,someid3'})		

	def test_queueVideo_should_call_get_batch_details_for_the_video_list(self):
		playlist_value = Mock()
		sys.modules["__main__"].xbmc.PlayList.return_value = playlist_value
		sys.modules["__main__"].core.getBatchDetails.return_value = ({"apierror":""},303)
		control = YouTubePlaylistControl()
		control.getPlayList = Mock()
		control.getPlayList.return_value = [{"Title":"someTitle1", "videoid":"some_id1","thumbnail":"some_thumbnail1"},{"Title":"someTitle2", "videoid":"some_id2","thumbnail":"some_thumbnail2"}]
		
		control.queueVideo({"videoid":"someid1,someid2,someid3"})
		
		sys.modules["__main__"].core.getBatchDetails.assert_called_with(['someid1', 'someid2', 'someid3'], {'videoid': 'someid1,someid2,someid3'})		

	def test_queueVideo_should_show_error_message_if_get_batch_details_fails(self):
		playlist_value = Mock()
		sys.modules["__main__"].xbmc.PlayList.return_value = playlist_value
		sys.modules["__main__"].language.return_value = ""
		sys.modules["__main__"].core.getBatchDetails.return_value = ([],303)
		control = YouTubePlaylistControl()
		control.getPlayList = Mock()
		control.getPlayList.return_value = [{"Title":"someTitle1", "videoid":"some_id1","thumbnail":"some_thumbnail1"},{"Title":"someTitle2", "videoid":"some_id2","thumbnail":"some_thumbnail2"}]
		
		control.queueVideo({"videoid":"someid1,someid2,someid3"})
		
		sys.modules["__main__"].utils.showErrorMessage.assert_called_with("","apierror",303)

	def test_queueVideo_should_correctly_queue_all_items_in_result_list(self):
		playlist_value = Mock()
		sys.modules["__main__"].xbmc.PlayList.return_value = playlist_value
		sys.modules["__main__"].language.return_value = ""
		sys.modules["__main__"].core.getBatchDetails.return_value = ([{"Title":"someTitle1","videoid":"some_id1", "thumbnail":"thumbnail1","video_url":"some_url1"}, {"Title":"someTitle1","videoid":"some_id1", "thumbnail":"thumbnail1","video_url":"some_url1"}, {"Title":"someTitle1","videoid":"some_id1", "thumbnail":"thumbnail1","video_url":"some_url1"}], 200)
		sys.modules["__main__"].utils.makeAscii.return_value = ""
		control = YouTubePlaylistControl()
		control.getPlayList = Mock()
		control.getPlayList.return_value = [{"Title":"someTitle1", "videoid":"some_id1","thumbnail":"some_thumbnail1"},{"Title":"someTitle2", "videoid":"some_id2","thumbnail":"some_thumbnail2"}]
		
		control.queueVideo({"videoid":"someid1,someid2,someid3"})
		
		assert(playlist_value.add.call_count == 3)

	def test_getPlayList_should_call_feeds_list_all(self):
		control = YouTubePlaylistControl()
		
		control.getPlayList({"playlist":"some_playlist"})
		
		sys.modules["__main__"].feeds.listAll.assert_called_with({'user_feed': 'playlist', 'playlist': 'some_playlist'})

	def test_getPlayList_should_exit_cleanly_if_playlist_id_is_missing_from_params(self):
		control = YouTubePlaylistControl()
		
		control.getPlayList({})
		
		assert(sys.modules["__main__"].feeds.listAll.call_count == 0)

	def test_getWatchLater_should_call_scraper_scrapeWatchLater(self):
		sys.modules["__main__"].scraper.scrapeWatchLater.return_value = ("",303)
		control = YouTubePlaylistControl()
		
		control.getWatchLater({})
		
		sys.modules["__main__"].scraper.scrapeWatchLater.assert_called_with({})

	def test_getDiscoSearch_should_call_scraper_searchDisco(self):
		sys.modules["__main__"].scraper.searchDisco.return_value = ("",303)
		control = YouTubePlaylistControl()
		
		control.getDiscoSearch({})
		
		sys.modules["__main__"].scraper.searchDisco.assert_called_with({})

	def test_getDiscoSearch_should_call_call_getBatchDetailsDisco_if_scraper_succeded(self):
		sys.modules["__main__"].scraper.searchDisco.return_value = ("",200)
		sys.modules["__main__"].core.getBatchDetails.return_value = ("",200)
		control = YouTubePlaylistControl()
		
		control.getDiscoSearch({})
		
		sys.modules["__main__"].scraper.searchDisco.assert_called_with({})
		sys.modules["__main__"].core.getBatchDetails.assert_called_with("", {})
		
	def test_getFavorites_should_exit_cleanly_if_contact_is_missing(self):
		sys.modules["__main__"].feeds.listAll.return_value = ("",200)
		control = YouTubePlaylistControl()
		
		control.getFavorites({})
		
		assert(sys.modules["__main__"].feeds.listAll.call_count == 0)

	def test_getFavorites_should_call_core_list_all_with_correct_params(self):
		sys.modules["__main__"].feeds.listAll.return_value = ("",200)
		control = YouTubePlaylistControl()
		
		control.getFavorites({"contact":"some_contact"})
		
		assert(sys.modules["__main__"].feeds.listAll.call_count == 1)
		sys.modules["__main__"].feeds.listAll.assert_called_with({"user_feed":"favorites","contact":"some_contact"})

	def test_getNewSubscriptions_should_exit_cleanly_if_contact_is_missing(self):
		sys.modules["__main__"].feeds.listAll.return_value = ("",200)
		control = YouTubePlaylistControl()
		
		control.getNewSubscriptions({})
		
		assert(sys.modules["__main__"].feeds.listAll.call_count == 0)

	def test_getNewSubscriptions_should_call_core_list_all_with_correct_params(self):
		sys.modules["__main__"].feeds.listAll.return_value = ("",200)
		control = YouTubePlaylistControl()
		
		control.getNewSubscriptions({"contact":"some_contact"})
		
		assert(sys.modules["__main__"].feeds.listAll.call_count == 1)
		sys.modules["__main__"].feeds.listAll.assert_called_with({"user_feed":"newsubscriptions","contact":"some_contact"})
		
	def test_getRecommended_should_exit_cleanly_if_login_or_scraper_is_not_in_params(self):
		control = YouTubePlaylistControl()
		
		control.getRecommended({})
		
		assert(sys.modules["__main__"].scraper.scrapeRecommended.call_count == 0)

	def test_getRecommended_should_call_scraper_getRecommended(self):
		sys.modules["__main__"].scraper.scrapeRecommended.return_value = ("",200)
		sys.modules["__main__"].core.getBatchDetails.return_value = ("",200)
		control = YouTubePlaylistControl()
		
		control.getRecommended({"login":"true","scraper":"recommended"})
		
		sys.modules["__main__"].scraper.scrapeRecommended.assert_called_with({"login":"true","scraper":"recommended"})

	def test_getRecommended_should_call_core_getBatchDetails_if_scraper_succeded(self):
		sys.modules["__main__"].scraper.scrapeRecommended.return_value = ("",200)
		sys.modules["__main__"].core.getBatchDetails.return_value = ("",200)
		control = YouTubePlaylistControl()
		
		control.getRecommended({"login":"true","scraper":"recommended"})
		
		sys.modules["__main__"].scraper.scrapeRecommended.assert_called_with({"login":"true","scraper":"recommended"})
		sys.modules["__main__"].core.getBatchDetails.assert_called_with("", {"login":"true","scraper":"recommended"})

	def test_getArtist_should_exit_cleanly_if_artist_is_not_in_params(self):
		control = YouTubePlaylistControl()
		
		control.getArtist({})
		
		assert(sys.modules["__main__"].scraper.scrapeArtist.call_count == 0)

	def test_getArtist_should_call_scraper_scrapeArtist(self):
		sys.modules["__main__"].scraper.scrapeArtist.return_value = ("",200)
		sys.modules["__main__"].core.getBatchDetails.return_value = ("",200)
		control = YouTubePlaylistControl()
		
		control.getArtist({"artist":"some_artist"})
		
		sys.modules["__main__"].scraper.scrapeArtist.assert_called_with({"artist":"some_artist"})

	def test_getArtist_should_call_core_getBatchDetails_if_scraper_succeded(self):
		sys.modules["__main__"].scraper.scrapeArtist.return_value = ("",200)
		sys.modules["__main__"].core.getBatchDetails.return_value = ("",200)
		control = YouTubePlaylistControl()
		
		control.getArtist({"artist":"some_artist"})
		
		sys.modules["__main__"].scraper.scrapeArtist.assert_called_with({"artist":"some_artist"})
		sys.modules["__main__"].core.getBatchDetails.assert_called_with("", {"artist":"some_artist"})
		
	def test_getLikedVideos_should_exit_cleanly_if_scraper_or_login_is_not_in_params(self):
		control = YouTubePlaylistControl()
		
		control.getLikedVideos({})
		
		assert(sys.modules["__main__"].scraper.scrapeLikedVideos.call_count == 0)
	
	def test_getLikedVideos_should_call_scraper_scrapeLikedVideos(self):
		sys.modules["__main__"].scraper.scrapeLikedVideos.return_value = ("",200)
		sys.modules["__main__"].core.getBatchDetails.return_value = ("",200)
		control = YouTubePlaylistControl()
		
		control.getLikedVideos({"login":"true","scraper":"liked_videos"})
		
		sys.modules["__main__"].scraper.scrapeLikedVideos.assert_called_with({"login":"true","scraper":"liked_videos"})
		
	def test_getLikedVideos_should_call_core_getBatchDetails_if_scraper_succeded(self):
		sys.modules["__main__"].scraper.scrapeLikedVideos.return_value = ("",200)
		sys.modules["__main__"].core.getBatchDetails.return_value = ("",200)
		control = YouTubePlaylistControl()
		
		control.getLikedVideos({"login":"true","scraper":"liked_videos"})
		
		sys.modules["__main__"].scraper.scrapeLikedVideos.assert_called_with({"login":"true","scraper":"liked_videos"})
		sys.modules["__main__"].core.getBatchDetails.assert_called_with("", {"login":"true","scraper":"liked_videos"})
		
	def test_addToPlaylist_should_call_list_all_if_playlist_is_not_in_params(self):
		sys.modules["__main__"].feeds.listAll.return_value = ([])
		control = YouTubePlaylistControl()
		
		control.addToPlaylist({})
		
		sys.modules["__main__"].feeds.listAll.assert_called_with({'user_feed': 'playlists', 'login': 'true', 'folder': 'true'})
		assert(sys.modules["__main__"].feeds.listAll.call_count == 1)

	def test_addToPlaylist_should_ask_user_for_playlist_if_playlist_is_not_in_params(self):
		sys.modules["__main__"].feeds.listAll.return_value = ([{"Title":"PlayList1"},{"Title":"PlayList2"}])
		sys.modules["__main__"].xbmcgui.Dialog().select.return_value = 0
		control = YouTubePlaylistControl()
		control.createPlayList = Mock()

		control.addToPlaylist({})
		
		assert(sys.modules["__main__"].xbmcgui.Dialog.call_count == 2)
		assert(sys.modules["__main__"].xbmcgui.Dialog().select.call_count == 1)

	def test_addToPlaylist_should_call_createPlaylist_if_user_selects_create_option(self):
		sys.modules["__main__"].xbmcgui.Dialog().select.return_value = 0
		sys.modules["__main__"].feeds.listAll.return_value = ([{"Title":"PlayList1"},{"Title":"PlayList2"}])
		control = YouTubePlaylistControl()
		control.createPlayList = Mock()
		
		control.addToPlaylist({})
		
		control.createPlayList.assert_called_with({'user_feed': 'playlists', 'login': 'true', 'folder': 'true'})

	def test_addToPlaylist_should_call_core_add_to_playlist_if_playlist_is_in_params(self):
		control = YouTubePlaylistControl()
		control.createPlayList = Mock()
		
		control.addToPlaylist({"playlist":"playlist1"})
		
		sys.modules["__main__"].core.add_to_playlist.assert_called_with({'playlist': 'playlist1'})

	def test_addToPlaylist_should_call_core_add_to_playlist_if_user_has_selected_playlist(self):
		sys.modules["__main__"].xbmcgui.Dialog().select.return_value = 1
		sys.modules["__main__"].feeds.listAll.return_value = ([{"Title":"PlayList1","playlist":"playlist1"},{"Title":"PlayList2","playlist":"playlist2"}])
		control = YouTubePlaylistControl()
		control.createPlayList = Mock()
		
		control.addToPlaylist({})
		
		sys.modules["__main__"].core.add_to_playlist.assert_called_with({'user_feed': 'playlists', 'login': 'true', 'playlist': 'playlist1', 'folder': 'true'})

	def test_createPlayList_should_ask_user_for_input(self):
		sys.modules["__main__"].utils.getUserInput.return_value = ""
		sys.modules["__main__"].xbmcgui.Dialog().select.return_value = 1
		sys.modules["__main__"].language.return_value = "my_string"
		control = YouTubePlaylistControl()
		
		control.createPlayList({})
		
		sys.modules["__main__"].utils.getUserInput.assert_called_with("my_string")
		sys.modules["__main__"].language.assert_called_with(30529)

	def test_createPlayList_should_call_addPlaylist_if_user_provided_playlist_name(self):
		sys.modules["__main__"].utils.getUserInput.return_value = "my_playlist_name"
		sys.modules["__main__"].xbmcgui.Dialog().select.return_value = 1
		sys.modules["__main__"].language.return_value = "my_string"
		control = YouTubePlaylistControl()
		
		control.createPlayList({})
		
		sys.modules["__main__"].core.add_playlist.assert_called_with({"title":"my_playlist_name"})
		
	def test_createPlayList_should_not_call_addPlaylist_if_user_cancels(self):
		sys.modules["__main__"].utils.getUserInput.return_value = ""
		sys.modules["__main__"].xbmcgui.Dialog().select.return_value = 1
		sys.modules["__main__"].language.return_value = "my_string"
		control = YouTubePlaylistControl()
		
		control.createPlayList({})
		
		assert(sys.modules["__main__"].core.add_playlist.call_count == 0)

		
	def test_removeFromPlaylist_should_exit_cleanly_if_playlist_or_playlist_entry_id_is_missing(self):
		control = YouTubePlaylistControl()
		
		control.removeFromPlaylist({})
		
		assert(sys.modules["__main__"].core.remove_from_playlist.call_count == 0)

	def test_removeFromPlaylist_should_call_core_remove_from_playlist(self):
		sys.modules["__main__"].core.remove_from_playlist.return_value = ("",200)
		control = YouTubePlaylistControl()

		control.removeFromPlaylist({"playlist_entry_id":"some_playlist_entry_id", "playlist":"some_playlist"})
		
		sys.modules["__main__"].core.remove_from_playlist.assert_called_with({"playlist_entry_id":"some_playlist_entry_id", "playlist":"some_playlist"})

	def test_removeFromPlaylist_should_show_error_message_if_remove_call_failed(self):
		sys.modules["__main__"].core.remove_from_playlist.return_value = ("fail",303)
		sys.modules["__main__"].language.return_value = "my_string"
		control = YouTubePlaylistControl()
		
		control.removeFromPlaylist({"playlist_entry_id":"some_playlist_entry_id", "playlist":"some_playlist"})
		
		sys.modules["__main__"].utils.showErrorMessage.assert_called_with("my_string","fail",303)
	
	def test_removeFromPlaylist_should_call_xbmc_execute_builtin_on_success(self):
		control = YouTubePlaylistControl()
		sys.modules["__main__"].core.remove_from_playlist.return_value = ("",200)
		
		control.removeFromPlaylist({"playlist_entry_id":"some_playlist_entry_id", "playlist":"some_playlist"})
		
		sys.modules["__main__"].xbmc.executebuiltin.assert_called_with("Container.Refresh")
	
	def test_deletePlaylist_should_exit_cleanly_if_playlist_is_missing(self):
		sys.modules["__main__"].core.remove_from_playlist.return_value = ("",200)
		control = YouTubePlaylistControl()
		
		control.deletePlaylist({})
		
		assert(sys.modules["__main__"].core.del_playlist.call_count == 0)
	
	def test_deletePlaylist_should_call_core_delete_playlist(self):
		sys.modules["__main__"].core.del_playlist.return_value = ("",200)
		control = YouTubePlaylistControl()
		
		control.deletePlaylist({"playlist":"some_playlist"})
		
		sys.modules["__main__"].core.del_playlist.assert_called_with({"playlist":"some_playlist"})
	
	def test_deletePlaylist_should_show_error_message_if_delete_call_failed(self):
		sys.modules["__main__"].core.del_playlist.return_value = ("fail",303)
		sys.modules["__main__"].language.return_value = "my_string"
		control = YouTubePlaylistControl()
		
		control.deletePlaylist({"playlist":"some_playlist"})
		
		sys.modules["__main__"].utils.showErrorMessage.assert_called_with("my_string","fail",303)
	
	def test_deletePlaylist_should_call_xbmc_execute_builtin_on_success(self):
		sys.modules["__main__"].core.del_playlist.return_value = ("",200)
		control = YouTubePlaylistControl()
		
		control.deletePlaylist({"playlist":"some_playlist_id"})
		
		sys.modules["__main__"].xbmc.executebuiltin.assert_called_with("Container.Refresh")	

if __name__ == '__main__':
	nose.runmodule()
