import React from "react";

export default function ResourceList({ resources }) {
  if (!resources) {
    return <p>Loading resources...</p>;
  }

  const {
    youtube_videos = [],
    coursera_courses = [],
    github_repos = []
  } = resources;

  if (
    youtube_videos.length === 0 &&
    coursera_courses.length === 0 &&
    github_repos.length === 0
  ) {
    return <p>No resources found.</p>;
  }

  return (
    <div className="space-y-6 mt-4">
      {youtube_videos.length > 0 && (
        <div>
          <h3 className="text-xl font-semibold mb-2">YouTube Videos</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {youtube_videos.map(video => (
              <div
                key={video.videoId}
                className="border rounded shadow p-2 bg-white"
              >
                <h4 className="font-medium text-center mb-2">{video.title}</h4>
                <iframe
                  width="100%"
                  height="225"
                  src={`https://www.youtube.com/embed/${video.videoId}`}
                  title={video.title}
                  frameBorder="0"
                  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                  allowFullScreen
                  className="rounded"
                ></iframe>
              </div>
            ))}
          </div>
        </div>
      )}

      {coursera_courses.length > 0 && (
        <div>
          <h3 className="text-xl font-semibold mb-2">Coursera Courses</h3>
          <ul className="space-y-2">
            {coursera_courses.map((course, index) => (
              <li key={index}>
                <a
                  href={course.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-600 hover:underline"
                >
                  {course.title}
                </a>
              </li>
            ))}
          </ul>
        </div>
      )}

      {github_repos.length > 0 && (
        <div>
          <h3 className="text-xl font-semibold mb-2">GitHub Repositories</h3>
          <ul className="space-y-2">
            {github_repos.map((repo, index) => (
              <li key={index}>
                <a
                  href={repo.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-600 hover:underline"
                >
                  {repo.repo}
                </a>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
