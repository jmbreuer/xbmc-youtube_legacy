# -*- coding: utf-8 -*-
import nose
import BaseTestCase
from mock import Mock, patch
import sys
from YouTubePlayer import YouTubePlayer


class TestYouTubePlayer(BaseTestCase.BaseTestCase):

    def test_getVideoUrlMap_should_return_empty_dictionary_on_missing_map(self):
        player = YouTubePlayer()

        result = player.getVideoUrlMap({"args": {}}, {})

        assert(result == {})

    def test_getVideoUrlMap_should_parse_streamMap(self):
        player = YouTubePlayer()

        result = player.getVideoUrlMap(self.readTestInput("streamMapTest.txt"), {})

        assert(len(result) == 11)
        keys = [5, 18, 22, 34, 35, 37, 43, 44, 45, 82, 84]
        for key in keys:
            assert(key in result)

    def test_getVideoUrlMap_should_parse_url_encoded_stream_map(self):
        player = YouTubePlayer()

        result = player.getVideoUrlMap(self.readTestInput("urlEncodedStreamMapTest.txt"), {})

        assert(len(result) == 11)
        keys = [5, 18, 22, 34, 35, 37, 43, 44, 45, 82, 84]
        for key in keys:
            assert(key in result)

    def test_getVideoUrlMap_should_parse_url_map(self):
        player = YouTubePlayer()

        result = player.getVideoUrlMap(self.readTestInput("urlMapTest.txt"), {})

        assert(len(result) == 11)
        keys = [5, 18, 22, 34, 35, 37, 43, 44, 45, 82, 84]
        for key in keys:
            assert(key in result)

    def test_getVideoUrlMap_should_parse_url_map_fallback(self):
        sys.modules["__main__"].settings.getSetting = Mock()
        sys.modules["__main__"].settings.getSetting.return_value = "false"

        player = YouTubePlayer()
        result = player.getVideoUrlMap(self.readTestInput("urlMapTest.txt"), {})
        print "BLA: " + str(len(result))
        assert(len(result) == 11)
        keys = [5, 18, 22, 34, 35, 37, 43, 44, 45, 82, 84]
        for key in keys:
            assert(key in result)
            assert(result[key].find("preferred") > result[key].find("fallback_host"))

    def test_getVideoUrlMap_should_mark_live_play(self):
        player = YouTubePlayer()
        video = {}

        result = player.getVideoUrlMap(self.readTestInput("liveStreamTest.txt"), video)

        assert(video["live_play"] == "true")
        assert(len(result) == 1)
        assert(34 in result)

    def test_playVideo_should_call_getVideoObject(self):
        player = YouTubePlayer()
        player.getVideoObject = Mock(return_value=[{"apierror": "some error"}, 303])

        player.playVideo()

        player.getVideoObject.assert_called_with({})

    def test_playVideo_should_log_and_fail_gracefully_on_apierror(self):
        player = YouTubePlayer()
        player.getVideoObject = Mock()
        player.getVideoObject.return_value = [{"apierror": "some error"}, 303]

        result = player.playVideo()

        assert(result == False)
        sys.modules["__main__" ].common.log.assert_called_with("construct video url failed contents of video item {'apierror': 'some error'}")

    def test_playVideo_should_call_xbmc_setResolvedUrl(self):
        sys.modules["__main__"].settings.getSetting.return_value = "0"
        player = YouTubePlayer()
        player.addSubtitles = Mock()
        player.getVideoObject = Mock()
        player.getVideoObject.return_value = ({"Title": "someTitle", "videoid": "some_id", "thumbnail": "someThumbnail", "video_url": "someUrl"}, 200)
        sys.argv = ["test1", "1", "test2"]

        player.playVideo({"videoid": "some_id"})

        assert(sys.modules["__main__"].xbmcplugin.setResolvedUrl.call_count > 0)

    def test_playVideo_should_call_addSubtitles(self):
        video = {"Title": "someTitle", "videoid": "some_id", "thumbnail": "someThumbnail", "video_url": "someUrl"}
        sys.modules["__main__"].settings.getSetting.return_value = "1"
        sys.argv = ["test1", "1", "test2"]
        player = YouTubePlayer()
        player.getVideoObject = Mock()
        player.getVideoObject.return_value = (video, 200)

        player.playVideo({"videoid": "some_id"})

        sys.modules["__main__"].subtitles.addSubtitles.assert_called_with(video)

    def test_playVideo_should_call_remove_from_watch_later_if_viewing_video_from_watch_later_queue(self):
        player = YouTubePlayer()
        sys.modules["__main__"].settings.getSetting.return_value = "0"
        sys.argv = ["test1", "1", "test2"]
        player.getVideoObject = Mock()
        player.getVideoObject.return_value = ({"Title": "someTitle", "videoid": "some_id", "thumbnail": "someThumbnail", "video_url": "someUrl"}, 200)
        player.addSubtitles = Mock()
        call_params = {"videoid": "some_id", "watch_later": "true", "playlist": "playlist_id", "playlist_entry_id": "entry_id"}

        player.playVideo(call_params)

        sys.modules["__main__"].core.remove_from_watch_later.assert_called_with(call_params)

    def test_playVideo_should_update_locally_stored_watched_status(self):
        sys.modules["__main__"].settings.getSetting.return_value = "0"
        sys.argv = ["test1", "1", "test2"]
        player = YouTubePlayer()
        player.getVideoObject = Mock()
        player.getVideoObject.return_value = ({"Title": "someTitle", "videoid": "some_id", "thumbnail": "someThumbnail", "video_url": "someUrl"}, 200)
        player.addSubtitles = Mock()

        player.playVideo({"videoid": "some_id"})
        sys.modules["__main__"].storage.storeValue.assert_called_with("vidstatus-some_id", "7" )

    def test_getInfo_should_use_cache_when_possible(self):
        sys.modules["__main__"].cache.get.return_value = '["something"]'
        player = YouTubePlayer()

        player.getInfo({"videoid": "some_id"})

        sys.modules["__main__"].cache.get.assert_called_with("videoidcachesome_id")

    def test_getInfo_should_call_fetchPage_with_correct_url(self):
        sys.modules["__main__"].cache.get.return_value = {}
        sys.modules["__main__"].core._fetchPage.return_value = {"status": 303, "content": "something"}
        player = YouTubePlayer()

        player.getInfo({"videoid": "some_id"})

        sys.modules["__main__"].core._fetchPage.assert_called_with({"api": "true", "link": player.urls["video_info"] % ("some_id")})

    def test_getInfo_should_call_core_getVideoInfo_to_parse_youtube_xml(self):
        sys.modules["__main__"].cache.get.return_value = {}
        sys.modules["__main__"].core._fetchPage.return_value = {"status": 200, "content": "something"}
        sys.modules["__main__"].core.getVideoInfo.return_value = [{"videoid": "some_id"}]
        player = YouTubePlayer()

        player.getInfo({"videoid": "some_id"})

        sys.modules["__main__"].core.getVideoInfo.assert_called_with("something", {"videoid": "some_id"})

    def test_getInfo_should_fail_correctly_if_api_is_unavailable(self):
        sys.modules["__main__"].cache.get.return_value = {}
        sys.modules["__main__"].core._fetchPage.return_value = {"status": 200, "content": "something"}
        sys.modules["__main__"].core.getVideoInfo.return_value = []
        sys.modules["__main__"].language.return_value = "some_string"
        player = YouTubePlayer()

        (video, status) = player.getInfo({"videoid": "some_id"})

        sys.modules["__main__"].common.log.assert_called_with("- Couldn't parse API output, YouTube doesn't seem to know this video id?")
        sys.modules["__main__"].language.assert_called_with(30608)
        assert(video["apierror"] == "some_string")

    def test_getInfo_should_save_video_info_in_cache(self):
        sys.modules["__main__"].cache.get.return_value = {}
        sys.modules["__main__"].core._fetchPage.return_value = {"status": 200, "content": "something"}
        sys.modules["__main__"].core.getVideoInfo.return_value = [{"videoid": "some_id"}]
        player = YouTubePlayer()

        (video, status) = player.getInfo({"videoid": "some_id"})

        sys.modules["__main__"].cache.set.assert_called_with('videoidcachesome_id', "{'videoid': 'some_id'}")

    def test_selectVideoQuality_should_prefer_h264_over_vp8_for_720p_as_appletv2_cant_handle_vp8_properly(self):
        sys.modules["__main__"].settings.getSetting.return_value = "2"
        player = YouTubePlayer()

        url = player.selectVideoQuality({22: "h264", 45: "vp8"}, {})

        assert(url == "h264 | Mozilla/5.0 (MOCK)")

    def test_selectVideoQuality_should_prefer_1080p_if_asked_to(self):
        sys.modules["__main__"].settings.getSetting.return_value = "2"
        player = YouTubePlayer()

        url = player.selectVideoQuality({37: "1080p", 22: "720p", 35: "SD"}, {"quality": "1080p"})

        assert(url == "1080p | Mozilla/5.0 (MOCK)")

    def test_selectVideoQuality_should_prefer_720p_if_asked_to(self):
        sys.modules["__main__"].settings.getSetting.return_value = "2"
        player = YouTubePlayer()

        url = player.selectVideoQuality({37: "1080p", 22: "720p", 35: "SD"}, {"quality": "720p"})

        assert(url == "720p | Mozilla/5.0 (MOCK)")

    def test_selectVideoQuality_should_prefer_SD_if_asked_to(self):
        sys.modules["__main__"].settings.getSetting.return_value = "2"
        player = YouTubePlayer()

        url = player.selectVideoQuality({37: "1080p", 22: "720p", 35: "SD"}, {"quality": "SD"})

        assert(url == "SD | Mozilla/5.0 (MOCK)")

    def test_selectVideoQuality_should_choose_highest_sd_quality_if_only_multiple_sd_qualities_are_available(self):
        sys.modules["__main__"].settings.getSetting.return_value = "1"
        player = YouTubePlayer()

        url = player.selectVideoQuality({5: "1", 33: "2", 18: "3", 26: "4", 43: "5", 34: "6", 78: "7", 44: "8", 59: "9", 35: "10"}, {})

        assert(url == "10 | Mozilla/5.0 (MOCK)")

    def test_selectVideoQuality_should_prefer_1080p_if_user_has_selected_that_option(self):
        sys.modules["__main__"].settings.getSetting.return_value = "3"
        player = YouTubePlayer()

        url = player.selectVideoQuality({35: "SD", 22: "720p", 37: "1080p"}, {})

        assert(url == "1080p | Mozilla/5.0 (MOCK)")

    def test_selectVideoQuality_should_limit_to_720p_if_user_has_selected_that_option(self):
        sys.modules["__main__"].settings.getSetting.return_value = "2"
        player = YouTubePlayer()

        url = player.selectVideoQuality({35: "SD", 22: "720p", 37: "1080p"}, {})

        assert(url == "720p | Mozilla/5.0 (MOCK)")

    def test_selectVideoQuality_should_limit_to_sd_if_user_has_selected_that_option(self):
        sys.modules["__main__"].settings.getSetting.return_value = "1"
        player = YouTubePlayer()

        url = player.selectVideoQuality({35: "SD", 22: "720p", 37: "1080p"}, {})

        assert(url == "SD | Mozilla/5.0 (MOCK)")

    def test_selectVideoQuality_should_call_userSelectsVideoQuality_if_user_selected_that_option(self):
        sys.modules["__main__"].settings.getSetting.return_value = "0"
        player = YouTubePlayer()
        player.userSelectsVideoQuality = Mock()

        player.selectVideoQuality({35: "SD", 22: "720p", 37: "1080p"}, {})

        player.userSelectsVideoQuality.assert_called_with({}, {35: 'SD', 37: '1080p', 22: '720p'})

    def test_selectVideoQuality_should_add_user_agent_when_not_called_by_download_function(self):
        sys.modules["__main__"].settings.getSetting.return_value = "1"
        player = YouTubePlayer()

        url = player.selectVideoQuality({35: "SD", 22: "720p", 37: "1080p"}, {})

        assert(url.find("| Mozilla/5.0 (MOCK)") > 0)

    def test_selectVideoQuality_should_not_add_user_agent_when_called_by_download_function(self):
        sys.modules["__main__"].settings.getSetting.return_value = "1"
        player = YouTubePlayer()

        url = player.selectVideoQuality({35: "SD", 22: "720p", 37: "1080p"}, {"action": "download"})

        assert(url.find("| Mozilla/5.0 (MOCK)") < 0)

    def test_userSelectsVideoQuality_should_append_list_of_known_qualities(self):
        sys.modules["__main__"].settings.getSetting.return_value = "1"
        sys.modules["__main__"].xbmcgui.Dialog().select.return_value = -1
        sys.modules["__main__"].language.return_value = ""
        player = YouTubePlayer()

        url = player.userSelectsVideoQuality({}, {35: "SD", 22: "720p", 37: "1080p", 35: "480p", 18: "380p", 34: "360p", 5: "240p", 17: "144p"})
        print repr(url)

        sys.modules["__main__"].xbmcgui.Dialog().select.assert_any_call("", ["1080p", "720p", "480p", "380p", "360p", "240p", "144p"])

    def test_userSelectsVideoQuality_should_prefer_h264_over_vp8_as_appletv2_cant_handle_vp8_properly(self):
        sys.modules["__main__"].settings.getSetting.return_value = "1"
        sys.modules["__main__"].xbmcgui.Dialog().select.return_value = 0
        sys.modules["__main__"].language.return_value = ""
        player = YouTubePlayer()

        url = player.userSelectsVideoQuality({}, {22: "h264", 45: "vp8"})

        assert(url == "h264")

    def test_userSelectsVideoQuality_should_select_proper_quality_based_on_user_input(self):
        player = YouTubePlayer()
        sys.modules["__main__"].settings.getSetting.return_value = "1"
        sys.modules["__main__"].xbmcgui.Dialog().select.return_value = 0
        sys.modules["__main__"].language.return_value = ""
        sys.modules["__main__"].common.makeUTF8.return_value = "bla"

        url = player.userSelectsVideoQuality({}, {35: "SD", 22: "720p", 37: "1080p"})

        sys.modules["__main__"].xbmcgui.Dialog().select.assert_called_with("", ["1080p", "720p", "480p"])
        assert(url == "1080p")

    def test_userSelectsVideoQuality_should_call_xbmc_dialog_select_to_ask_for_user_input(self):
        sys.modules["__main__"].settings.getSetting.return_value = "1"
        sys.modules["__main__"].xbmcgui.Dialog().select.return_value = -1
        sys.modules["__main__"].language.return_value = ""
        player = YouTubePlayer()

        url = player.userSelectsVideoQuality({}, {35: "SD", 22: "720p", 37: "1080p"})

        print repr(url)

        assert(sys.modules["__main__"].xbmcgui.Dialog().select.call_count > 0)

    def test_getVideoObject_should_get_video_information_from_getInfo(self):
        sys.modules["__main__"].settings.getSetting.return_value = ""
        player = YouTubePlayer()
        player.getInfo = Mock()
        player.getInfo.return_value = ({}, 303)
        player._getVideoLinks = Mock()
        player._getVideoLinks.return_value = ({}, {})

        player.getVideoObject({})

        player.getInfo.assert_called_with({})

    def test_getVideoObject_should_use_local_file_for_playback_if_found(self):
        sys.modules["__main__"].subtitles.getLocalFileSource.return_value = "somePath/someTitle.mp4"
        params = {"videoid": "some_id"}
        player = YouTubePlayer()
        player.getInfo = Mock()
        video = {"videoid": "some_id", "Title": "someTitle"}
        player.getInfo.return_value = (video, 200)

        (video, status) = player.getVideoObject(params)

        assert(video["video_url"] == "somePath/someTitle.mp4")

    def test_getVideoObject_should_not_scrape_webpage_if_local_file_is_found(self):
        sys.modules["__main__"].subtitles.getLocalFileSource.return_value = "somePath/someTitle.mp4"
        params = {"videoid": "some_id"}
        player = YouTubePlayer()
        player.getInfo = Mock()
        player._getVideoLinks = Mock()
        video = {"videoid": "some_id", "Title": "someTitle"}
        player.getInfo.return_value = (video, 200)

        player.getVideoObject(params)

        assert(player._getVideoLinks.call_count == 0)

    def test_getVideoObject_should_check_for_local_file_before_scraping(self):
        sys.modules["__main__"].subtitles.getLocalFileSource.return_value = "somePath/someTitle.mp4"
        params = {"videoid": "some_id"}
        player = YouTubePlayer()
        player.getInfo = Mock()
        video = {"videoid": "some_id", "Title": "someTitle"}
        player.getInfo.return_value = (video, 200)

        (video, status) = player.getVideoObject(params)

        sys.modules["__main__"].subtitles.getLocalFileSource.assert_called_with(params, video)

    def test_getVideoObject_should_call_getVideoLinks_if_local_file_not_found(self):
        sys.modules["__main__"].subtitles.getLocalFileSource.return_value = ""
        params = {"videoid": "some_id"}
        player = YouTubePlayer()
        player.getInfo = Mock()
        player._getVideoLinks = Mock()
        player._getVideoLinks.return_value = ({}, {})
        video = {"videoid": "some_id", "Title": "someTitle"}
        player.getInfo.return_value = (video, 200)

        player.getVideoObject(params)

        player._getVideoLinks.assert_any_call(video, params)

    def test_getVideoObject_should_call_selectVideoQuality_if_local_file_not_found_and_remote_links_found(self):
        sys.modules["__main__"].subtitles.getLocalFileSource.return_value = ""
        params = {"videoid": "some_id"}
        video = {"videoid": "some_id", "Title": "someTitle"}

        player = YouTubePlayer()
        player.getInfo = Mock()
        player.getInfo.return_value = (video, 200)

        player._getVideoLinks = Mock()
        player._getVideoLinks.return_value = ({22: "720p"}, {})
        player.selectVideoQuality = Mock()

        player.getVideoObject(params)

        player.selectVideoQuality.assert_called_with({22: "720p"}, params)

    def test_getVideoObject_should_use_pre_defined_error_messages_on_missing_url(self):
        sys.modules["__main__"].settings.getSetting.return_value = ""
        player = YouTubePlayer()
        player.getInfo = Mock()
        player.getInfo.return_value = ({}, 303)
        player.getLocalFileSource = Mock(return_value="")
        player._getVideoLinks = Mock(return_value = ({}, {}))

        player.getVideoObject({})

        player.getInfo.assert_called_with({})
        sys.modules["__main__"].language.assert_called_with(30618)

    def test_convertFlashVars_should_parse_html_properly(self):
        player = YouTubePlayer()

        result = player._convertFlashVars(self.readTestInput("flashVarsTest.html", False))
        print "RESULT: " + repr(result)
        assert(len(result["args"]) == 77)

    def test_getVideoLinks_should_try_scraping_first(self):
        player = YouTubePlayer()
        sys.modules["__main__"].core._fetchPage.return_value = {"status": 200, "content": "something"}
        sys.modules["__main__"].common.parseDOM.return_value = ""
        sys.modules["__main__"].common.extractJS.return_value = [{"args": ""}]

        player._getVideoLinks({}, {"videoid": "some_id"})

        sys.modules["__main__"].core._fetchPage.assert_called_with({"link": player.urls["video_stream"] % ("some_id")})

    def test_getVideoLinks_should_fall_back_to_embed(self):
        sys.modules["__main__"].core._fetchPage.return_value = {"status": 303, "content": "something"}
        player = YouTubePlayer()

        player._getVideoLinks({}, {"videoid": "some_id"})

        sys.modules["__main__"].core._fetchPage.assert_called_with({"link": player.urls["embed_stream"] % ("some_id")})

    def test_getVideoLinks_should_get_error_message_from_embed(self):
        sys.modules["__main__"].core._fetchPage.return_value = {"status": 303, "content": self.readTestInput("watch-gyzlwNvf8ss-get_video_info.txt", False)}

        player = YouTubePlayer()
        result = player._getVideoLinks({}, {"videoid": "some_id"})
        print repr(result)
        assert(result[0] == [])
        assert(result[1] == {'apierror': u'Ugyldige parametre.'})

    def test_getVideoLinks_should_parse_flashvars_from_embed(self):
        player = YouTubePlayer()

        sys.modules["__main__"].core._fetchPage.side_effect = [{"status": 500, "content": self.readTestInput("get_video_info-gyzlwNvf8ss", False)}, {"status": 200, "content": self.readTestInput("get_video_info-gyzlwNvf8ss", False)} ]
        sys.modules["__main__"].common.parseDOM.return_value = [self.readTestInput("watch-gyzlwNvf8ss-flashvars.txt", False) ]

        result = player._getVideoLinks({}, {"videoid": "some_id"})
        print repr(result)
        assert(result == self.readTestInput("flashvars-gyzlwNvf8ss-map-test-embed.txt"))

    def test_getVideoLinks_should_call_getVideoUrlMap(self):
        player = YouTubePlayer()
        player.getVideoUrlMap = Mock()
        player.getVideoUrlMap.return_value = {}

        sys.modules["__main__"].core._fetchPage.side_effect = [{"status": 500, "content": self.readTestInput("get_video_info-gyzlwNvf8ss", False)}, {"status": 200, "content": self.readTestInput("get_video_info-gyzlwNvf8ss", False)} ]
        sys.modules["__main__"].common.parseDOM.return_value = [self.readTestInput("watch-gyzlwNvf8ss-flashvars.txt", False) ]
        sys.modules["__main__"].core._findErrors.return_value = "mock error"

        result = player._getVideoLinks({}, {"videoid": "some_id"})

        print repr(result)

        assert(player.getVideoUrlMap.call_args_list[0][0] == self.readTestInput("watch-gyzlwNvf8ss-getVideoUrlMap-call.txt"))

if __name__ == '__main__':
    nose.runmodule()
