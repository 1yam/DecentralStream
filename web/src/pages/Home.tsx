import {Sidebar, Spinner} from "flowbite-react";
import {useEffect, useState} from "react";
import axios from "axios";
import ReactPlayer from "react-player";

export default function Home() {
  const [streamersLoading, setStreamersLoading] = useState(false)
  const [streamers, setStreamers] = useState([])

  const [selectedStreamer, setSelectedStreamer] = useState("")

  const fetchStreamers = async () => {
    setStreamersLoading(true)
    try {
      const response = await axios.get('/streams')
      setStreamers(response.data.online_streamer)
    } catch (error) {
      console.log(error)
    }
    setStreamersLoading(false)
  }

  const selectedStreamerUrl = () => {
    if (!selectedStreamer) return ""

    return `http://localhost:8000/hls/${selectedStreamer}/playlist.m3u8`
  }

  useEffect(() => {
    fetchStreamers()
  }, [])


  if (streamersLoading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <Spinner/>
      </div>
    )
  }

  return (
    <div>
      <section className="bg-white dark:bg-gray-900">
        <div className="flex max-w-screen-xl px-4 py-8 mx-auto gap-8">
          <div className={'w-1/4'}>
            <Sidebar className={'w-full'}>
              <Sidebar.ItemGroup>
                <h1 className={'text-lg text-center font-medium'}>Active streamers</h1>
              </Sidebar.ItemGroup>
              <Sidebar.ItemGroup>
                {!streamers.length && (
                  <p className={'text-center text-gray-500 dark:text-gray-400'}>No streamers online</p>
                )}

                {streamers.map((streamer: string, idx: number) => (
                  <Sidebar.Items key={idx}>
                    <Sidebar.ItemGroup>
                      <Sidebar.Item className={'cursor-pointer'} active={streamer === selectedStreamer}
                                    onClick={() => setSelectedStreamer(streamer)}>
                        <span className={'break-all text-wrap'}>
                          {streamer}
                        </span>
                      </Sidebar.Item>
                    </Sidebar.ItemGroup>
                  </Sidebar.Items>
                ))}
              </Sidebar.ItemGroup>
            </Sidebar>
          </div>
          <div className={'w-3/4'}>
            <div className="lg:col-span-12">
              {!selectedStreamer ? (
                <p className={'text-center text-gray-500 dark:text-gray-400'}>Select a streamer to watch</p>
              ) : (
                <>
                  <h1 className={'text-center text-lg font-medium'}>Watching {selectedStreamer}</h1>

                  <ReactPlayer
                    url={selectedStreamerUrl()}
                    options={{
                      forceHLS: true
                    }}
                    controls
                    width="100%"
                    height="100%"
                    className="mt-4"
                  />
                </>
              )}
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}