var folder_path = "../test_images"

app.EnableNewWorld = false;
//var videoTracks = app.project.sequences[0].audioTracks;
var videoTracks = app.project.activeSequence.videoTracks;
//var firstTrack = videoTracks[0].clips[0].setSelected(1, 1);
var firstTrack = videoTracks[0];
//firstTrack.setSelected(1,1);
//firstTrack.remove(1, 1);
alert(String(firstTrack));
//app.project.importFiles("../test_images", 1);
firstTrack.setMuted = true;
videoTracks[0].setMuted = true;

var filterString = "";
if (Folder.fs === 'Windows') {
    filterString = "All files:*.*";
}

//for(var i=0; i< app.project.rootItem.children.length; i++) {
  //  alert(String(app.project.rootItem.children[i].findItemsMatchingMediaPath("F:\Video Resources\Albert_Ein\images\image1.jpg", 0)))
//}
if (app.project) {
    var fileOrFilesToImport = File.openDialog(	"Choose files to import", // title
                                                filterString, // filter available files?
                                                true); // allow multiple?
    if (fileOrFilesToImport) {
        // We have an array of File objects; importFiles() takes an array of paths.
        var importThese = [];
        if (importThese) {
            for (var i = 0; i < fileOrFilesToImport.length; i++) {
                importThese[i] = fileOrFilesToImport[i].fsName;
                alert(String(fileOrFilesToImport[i].nodeId));
                //var vTrack = seq.videoTracks[0];

            // set start time
            var time1 = new Time();
            //time1.seconds = startTime; // this value comes from an array

            // get media item
            //var mediaItem = getProjectItemByName(app.project.getInsertionBin(), mediaName, ProjectItemType.CLIP);

            // insert clip at start time
            app.project.rootItem.children[0].attachProxy(fileOrFilesToImport[i].fsName, 1);
            

            // set end time
            var time2 = new Time();
            //time2.seconds = endTime;
            //vTrack.clips[itemIndex].end = time2;
            //itemIndex++;
            }
            var suppressWarnings 	= true;
            var importAsStills		= true;
            app.project.importFiles(importThese,
                                    suppressWarnings,
                                    app.project.getInsertionBin(),
                                    importAsStills, 0);
        }
    } else {
        $._PPP_.updateEventPanel("No files to import.");
    }
}

var seq = app.project.activeSequence;
		if (seq) {
			var first = app.project.rootItem.children[0];
			if (first) {
				if (!first.isSequence()) {
					if (first.type !== ProjectItemType.BIN) {
						var numVTracks = seq.videoTracks.numTracks;
						var targetVTrack = seq.videoTracks[(numVTracks - 1)];
						if (targetVTrack) {
							// If there are already clips in this track, append this one to the end. Otherwise, insert at start time.
							if (targetVTrack.clips.numItems > 0) {
								var lastClip = targetVTrack.clips[(targetVTrack.clips.numItems - 1)];
								if (lastClip) {
									targetVTrack.insertClip(first, lastClip.end.seconds);
								}
							} else {
								var timeAtZero = new Time();
								targetVTrack.insertClip(first, timeAtZero.seconds);
								// Using linkSelection/unlinkSelection calls, panels can remove just the audio (or video) of a given clip.
								var newlyAddedClip = targetVTrack.clips[(targetVTrack.clips.numItems - 1)];
								if (newlyAddedClip) {
									newlyAddedClip.setSelected(true, true);
									seq.unlinkSelection();
									newlyAddedClip.remove(true, true);
									seq.linkSelection();
								} else {
									$._PPP_.updateEventPanel("Could not add clip.");
								}
							}
						} else {
							$._PPP_.updateEventPanel("Could not find first video track.");
						}
					} else {
						$._PPP_.updateEventPanel(first.name + " is a bin.");
					}
				} else {
					$._PPP_.updateEventPanel(first.name + " is a sequence.");
				}
			} else {
				$._PPP_.updateEventPanel("Couldn't locate first projectItem.");
			}
		} else {
			$._PPP_.updateEventPanel("no active sequence.");
		}
