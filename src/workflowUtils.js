
// XML utility functions for sanitizing input text

export const generateInitialXml = (documentText) => {
  // Escape the 5 special XML characters
  const escapedText = documentText
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&apos;');

  const finalXml = `<?xml version="1.0" encoding="UTF-8"?>
<Document>${escapedText}</Document>`;

  return finalXml;
};
