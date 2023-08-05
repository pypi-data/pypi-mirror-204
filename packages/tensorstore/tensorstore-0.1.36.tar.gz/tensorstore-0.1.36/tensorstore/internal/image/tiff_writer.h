// Copyright 2022 The TensorStore Authors
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#ifndef TENSORSTORE_INTERNAL_IMAGE_TIFF_WRITER_H_
#define TENSORSTORE_INTERNAL_IMAGE_TIFF_WRITER_H_

#include <memory>
#include <utility>

#include "absl/status/status.h"
#include "riegeli/bytes/writer.h"
#include "tensorstore/internal/image/image_info.h"
#include "tensorstore/internal/image/image_writer.h"
#include "tensorstore/util/span.h"

namespace tensorstore {
namespace internal_image {

struct TiffWriterOptions {};

class TiffWriter : public ImageWriter {
 public:
  struct Context;

  TiffWriter();
  ~TiffWriter() override;
  TiffWriter(TiffWriter&& src);
  TiffWriter& operator=(TiffWriter&& src);

  // Initialize the codec. This is not done in the constructor in order
  // to allow returning errors to the caller.
  absl::Status Initialize(riegeli::Writer* writer) override {
    return InitializeImpl(std::move(writer), {});
  }
  absl::Status Initialize(riegeli::Writer* writer,
                          const TiffWriterOptions& options) {
    return InitializeImpl(std::move(writer), options);
  }

  // Encodes image with the provided options.
  absl::Status Encode(const ImageInfo& info,
                      tensorstore::span<const unsigned char> source) override;

  /// Finish writing. Closes the writer and returns the status.
  absl::Status Done() override;

 private:
  absl::Status InitializeImpl(riegeli::Writer* writer,
                              const TiffWriterOptions& options);

  std::unique_ptr<Context> context_;
};

}  // namespace internal_image
}  // namespace tensorstore

#endif  // TENSORSTORE_INTERNAL_IMAGE_TIFF_WRITER_H_
