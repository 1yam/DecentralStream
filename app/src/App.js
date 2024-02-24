import {useEffect, useState} from "react";
import ReactPlayer from "react-player";


function App() {
  // const [cids, setCids] = useState([])
  // const [currentCid, setCurrentCid] = useState(null)
  // const [nextCid, setNextCid] = useState(null)
  //
  // function fetchCids() {
  //   fetch('http://localhost:5000/get_cid/StreamTest')
  //     .then(response => response.json())
  //     .then(data => {
  //       if (data.cids.length > 10) {
  //         return
  //       }
  //
  //       setCids(data.cids)
  //
  //       if (currentCid === null) {
  //         setCurrentCid(data.cids[data.cids.length - 10].split(':')[1])
  //       } else {
  //         // check if new cid is available
  //         if (data.cids[data.cids.length - 10] !== currentCid) {
  //           setNextCid(data.cids[0].split(':')[1])
  //         }
  //       }
  //     });
  // }
  //
  // useEffect(() => {
  //   //setInterval(fetchCids, 5000)
  //   //fetchCids()
  // }, [])

  const config = {
    file: {
      forceHLS: true
    }
  }

  return (
    <div className="App">
      {/*{currentCid !== null ?<ReactPlayer*/}
      {/*  url={`http://localhost:8000/video?hash=${currentCid}`}*/}
      {/*  controls*/}
      {/*  playing*/}
      {/*  onEnded={() => setCurrentCid(nextCid)}*/}
      {/*/> : <div>loading...</div>}*/}
      Hello world

      <ReactPlayer config={config}  url={'http://localhost:8000/files/playlist.m3u8'} controls playing />
    </div>
  );
}

export default App;
