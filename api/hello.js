export default function handler(request, response) {
  return response.status(200).json({
    message: 'Business Finder API is working!',
    status: 'success'
  });
}
