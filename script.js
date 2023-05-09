function displayMessages(data) {
	// Get the HTML element where the messages will be displayed
	const messagesDiv = document.getElementById('messages')

	// Create a map to store the CSS class for each participant
	const participantClasses = {}

	let counter = 0

	// Color
	const colors = [
		'#7c1158',
		'#0d4c73',
		'#213388',
		'#113910',
		'#6E3C8E',
		'#689F38',
		'#35495E',
		'#AFB42B',
		'#8C3C72',
		'#621111',
	]

	// Loop through the participants and assign a color to each one
	data.participants.forEach((participant, index) => {
		// Get the index of the color to assign to this participant
		const colorIndex = index % colors.length

		// Get the color from the array
		const color = colors[colorIndex]

		// Create a CSS class for the participant
		const participantClass = `.sender-${participant.name.toLowerCase().replace(/\s+/g, '-')}`
		participantClasses[participant.name] = participantClass

		// Add the CSS rules for the class to the page
		const style = document.createElement('style')
		style.type = 'text/css'
		style.innerHTML = `${participantClass} { color: ${color}; }`
		document.getElementsByTagName('head')[0].appendChild(style)
	})

	// Messages

	// Create HTML elements for each message and append them to the messagesDiv
	data.messages.forEach((message) => {
		// Skip messages with is_unsent = true
		// if (message.is_unsent) {
		// 	return
		// }

		const messageDiv = document.createElement('div')
		messageDiv.classList.add('message')
		messageDiv.setAttribute('id', message.timestamp_ms)

		// Counter

		counter += 1

		// Timestamp

		const timestampDiv = document.createElement('div')
		timestampDiv.classList.add('timestamp')
		const timestamp = new Date(message.timestamp_ms)
		const options = {
			year: 'numeric',
			month: '2-digit',
			day: '2-digit',
			hour: '2-digit',
			minute: '2-digit',
			second: '2-digit',
			hour12: false,
		}
		const dateStr = timestamp.toLocaleString('en-GB', options)
		const dayStr = timestamp.toLocaleString('en-GB', { weekday: 'short' })
		// prevent from copying: user-select: none;
		timestampDiv.innerHTML = `<span style="color: #aaa; font-family: Consolas; cursor: pointer;">${dateStr}, ${dayStr}, #${counter}</span>`
		messageDiv.appendChild(timestampDiv)

		timestampDiv.addEventListener('click', function () {
			window.location.hash = message.timestamp_ms
		})

		// Sender

		const senderNameDiv = document.createElement('div')
		senderNameDiv.classList.add('sender-name')
		senderNameDiv.classList.add(`sender-${message.sender_name.toLowerCase().replace(/\s+/g, '-')}`) // Add the CSS class for the sender
		senderNameDiv.innerText = message.sender_name
		messageDiv.appendChild(senderNameDiv)

		// Content

		const contentDiv = document.createElement('div')
		contentDiv.classList.add('content')
		const content = message.content || ''
		if (content.match(/(?:https?):\/\/[^\s]+/)) {
			const urlRegex = /(https?:\/\/[^\s]+)/g
			contentDiv.innerHTML = content.replace(urlRegex, '<a href="$1" target="_blank">$1</a>')
		} else {
			// change to this for italics: contentDiv.innerHTML = content.replace(/_([^_]+)_/g, '<em>$1</em>')
			contentDiv.innerText = content
		}
		messageDiv.appendChild(contentDiv)

		// Files

		if (message.files) {
			message.files.forEach((file) => {
				const fileLink = document.createElement('a')
				const src = file.uri.replace(/^.*[\\\/]/, '') // remove everything before the last / or \
				fileLink.href = 'files/' + src
				fileLink.download = src.split('/').pop() // set download attribute to the filename

				const fileIcon = document.createElement('i')
				fileIcon.classList.add('fas', 'fa-file')

				const fileName = document.createElement('span')
				fileName.textContent = src.split('/').pop()
				fileName.style.color = 'indianred'

				const fileDiv = document.createElement('div')
				fileDiv.classList.add('file')
				fileDiv.appendChild(fileIcon)
				fileDiv.appendChild(fileName)

				messageDiv.appendChild(fileLink)
				fileLink.appendChild(fileDiv)
			})
		}

		// Videos

		if (message.videos && message.videos.length > 0) {
			const videosDiv = document.createElement('div')
			videosDiv.classList.add('videos')
			message.videos.forEach((video) => {
				const videoDiv = document.createElement('div')
				const videoElement = document.createElement('video')

				const videoSrc = video.uri.replace(/^.*[\\\/]/, 'videos/')
				videoElement.src = videoSrc
				videoElement.controls = true

				const videoFileName = video.uri.split('/').pop()

				const fileNameElement = document.createElement('p')
				fileNameElement.textContent = videoFileName
				fileNameElement.setAttribute('style', 'color: #aaa; font-size: 5px; margin: 0; padding: 0;')

				videoDiv.appendChild(videoElement)
				videoDiv.appendChild(fileNameElement)
				videosDiv.appendChild(videoDiv)
			})
			messageDiv.appendChild(videosDiv)
		}

		// Photos

		if (message.photos) {
			message.photos.forEach((photo) => {
				const photoImg = document.createElement('img')
				const src = photo.uri.replace(/^.*[\\\/]/, '') // remove everything before the last / or \
				photoImg.src = 'photos/' + src
				photoImg.classList.add('photo')

				messageDiv.appendChild(photoImg)
			})
		}

		if (message.photos) {
			message.photos.forEach((photo) => {
				const photoFileName = photo.uri.split('/').pop()
				const fileNameElement = document.createElement('p')
				fileNameElement.textContent = photoFileName
				fileNameElement.setAttribute('style', 'color: #aaa; font-size: 5px; margin: 0; padding: 0;')

				messageDiv.appendChild(fileNameElement)
			})
		}

		// GIFs

		if (message.gifs) {
			message.gifs.forEach((gif) => {
				const gifImg = document.createElement('img')
				const src = gif.uri.replace(/^.*[\\\/]/, '') // remove everything before the last / or \
				gifImg.src = 'gifs/' + src
				gifImg.classList.add('gif')

				const gifFileName = gif.uri.split('/').pop()

				const fileNameElement = document.createElement('p')
				fileNameElement.textContent = gifFileName
				fileNameElement.setAttribute('style', 'color: #aaa; font-size: 5px; margin: 0; padding: 0;')

				messageDiv.appendChild(gifImg)
				messageDiv.appendChild(fileNameElement)
			})
		}

		// Audio

		if (message.audio_files) {
			message.audio_files.forEach((audio) => {
				const audioElement = document.createElement('audio')
				audioElement.controls = true
				const src = audio.uri.replace(/^.*[\\\/]/, '') // remove everything before the last / or \
				audioElement.src = 'audio/' + src

				const audioFileName = audio.uri.split('/').pop()

				const fileNameElement = document.createElement('p')
				fileNameElement.textContent = audioFileName
				fileNameElement.setAttribute('style', 'color: #aaa; font-size: 5px; margin: 0; padding: 0;')

				messageDiv.appendChild(audioElement)
				messageDiv.appendChild(fileNameElement)
			})
		}

		messagesDiv.appendChild(messageDiv)
	})
}

// Load the local JSON file
// const messages = require('./message_1.json')

// Pass the JSON data to the function to display the messages in HTML
// displayMessages(messages)
